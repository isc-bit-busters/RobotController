from pathfinder import navmesh_baker as nmb
import pathfinder as pf
import numpy
import trimesh
import time

# We're generating our navmesh in pixel space, but the navmesh baker
# gets really slow with a scale that big (in the thousandss).
# So we scale down the polygons to a more reasonable size.
SCALE = 50
AGENT_RADIUS_SCALED = 0.43 # In scaled space
AGENT_RADIUS_REAL = AGENT_RADIUS_SCALED * SCALE # In real space

# def generate_navmesh(input_file="polygons.txt", output_file="navmesh.txt"):
def generate_navmesh(polygons):
    # polygons = polygons.reshape(-1, 4)
    polygons = numpy.array(polygons) / SCALE
    max_x, max_y = polygons[:, 0].max(), polygons[:, 1].max()

    # polygons = polygons[(polygons[:, 2] > 0.1) & (polygons[:, 3] > 0.1)]

    wall_blocks = []
    for wall in polygons:
        x, y, w, h = wall
        w = abs(w - x)
        h = abs(h - y)

        # Ensure the wall is not too small
        if w < 0.1:
            w = 0.1
        if h < 0.1:
            h = 0.1

        block = trimesh.creation.box(extents=(w, 6, h))

        # Trimesh mesh position is at the center of the mesh 
        # Our polygons are defined by the top left corner
        block.apply_translation((x + w / 2, 0, y + h / 2))

        wall_blocks.append(block)

    plane = trimesh.creation.box(extents=(max_x, 0.1, max_y))
    plane.apply_translation((max_x/2, 0, max_y/2))

    meshes = [plane, *wall_blocks]

    all_vertices = []
    all_faces = []
    vertex_offset = 0

    # Convert meshes to vertices + faces as list vertices indices
    for mesh in meshes:
        vertices = mesh.vertices
        faces = mesh.faces

        all_vertices.extend(vertices)

        offset_faces = []
        for face in faces:
            offset_face = [idx + vertex_offset for idx in face]
            offset_faces.append(offset_face)

        all_faces.extend(offset_faces)

        vertex_offset += len(vertices)

    baker = nmb.NavmeshBaker()

    baker.add_geometry(
        vertices=all_vertices,
        polygons=all_faces,
    )

    baker.bake(
        agent_radius=AGENT_RADIUS_SCALED,   # TODO: unhardcode this
        cell_size=0.04,   # TODO: unhardcode this
        # verts_per_poly=3
    )

    baker.save_to_text("/agent/navmesh_raw.txt")

    return baker.get_polygonization()

def find_path(start, end, vertices, polygons):
    start = numpy.array(start) / SCALE
    init_start = start
    end = numpy.array(end) / SCALE
    pathfinder = pf.PathFinder(vertices, polygons)

    sampled_start = pathfinder.sample(start)
    sampled_end = pathfinder.sample(end)

    start = sampled_start if sampled_start is not None else start
    end = sampled_end if sampled_end is not None else end

    print(f"Start: {start} - {init_start}")
    print(f"End: {end}")

    path = pathfinder.search_path(start, end)

    if path is not None:
        path = numpy.array(path) * SCALE

    return path

def find_path_two_bots(start1, end1, start2, end2, vertices, polygons):
    pathfinder = pf.PathFinder(
        vertices, 
        polygons,
        neighbor_dist=50,
    )

    start1, start2, end1, end2 = numpy.array(start1) / SCALE, numpy.array(start2) / SCALE, numpy.array(end1) / SCALE, numpy.array(end2) / SCALE

    start1 = pathfinder.sample(start1) or start1
    end1 = pathfinder.sample(end1) or end1

    start2 = pathfinder.sample(start2) or start2
    end2 = pathfinder.sample(end2) or end2

    agent_one = pathfinder.add_agent(
        start1,
        AGENT_RADIUS_SCALED * 1.5,
        1,
    )

    agent_two = pathfinder.add_agent(
        start2,
        AGENT_RADIUS_SCALED * 1.5,
        1,
    )

    pathfinder.set_agent_destination(agent_one, end1)
    pathfinder.set_agent_destination(agent_two, end2)

    paths = pathfinder.get_all_agents_paths()

    pathfinder._obstacles

    paths = [numpy.array(path) * SCALE for path in paths]

    return paths

def find_collision(path1, path2, step_dist=0.1, robot_radius=AGENT_RADIUS_REAL):
    if len(path1) < 1 or len(path2) < 1:
        print("Path too short to check for collision:")
        print(len(path1), len(path2))
        return None

    robot_radius *= 1.5

    path1 = numpy.array(path1)
    path2 = numpy.array(path2)

    # Pad the shorter path with its last point to match lengths
    if len(path1) < len(path2):
        last_point = path1[-1].reshape(1, -1)
        padding = numpy.tile(last_point, (len(path2) - len(path1), 1))
        path1 = numpy.vstack((path1, padding))
    elif len(path2) < len(path1):
        last_point = path2[-1].reshape(1, -1)
        padding = numpy.tile(last_point, (len(path1) - len(path2), 1))
        path2 = numpy.vstack((path2, padding))
    
    # Pre-compute path segments and lengths once
    segments1 = []
    segments2 = []
    segment_lengths1 = []
    segment_lengths2 = []
    
    # Compute segments and their lengths for path1
    for i in range(len(path1) - 1):
        p1, p2 = path1[i], path1[i + 1]
        segments1.append((p1, p2))
        segment_lengths1.append(numpy.linalg.norm(p2 - p1))
    
    # Compute segments and their lengths for path2
    for i in range(len(path2) - 1):
        p1, p2 = path2[i], path2[i + 1]
        segments2.append((p1, p2))
        segment_lengths2.append(numpy.linalg.norm(p2 - p1))
    
    # Calculate total path distances
    dist_path1 = sum(segment_lengths1)
    dist_path2 = sum(segment_lengths2)
    max_dist = max(dist_path1, dist_path2)
    
    # Create lookup tables for quick path location access
    path1_lookup = [(0, 0)]  # (segment_idx, accumulated_distance)
    accumulated = 0
    for i, length in enumerate(segment_lengths1):
        accumulated += length
        path1_lookup.append((i+1, accumulated))
    
    path2_lookup = [(0, 0)]
    accumulated = 0
    for i, length in enumerate(segment_lengths2):
        accumulated += length
        path2_lookup.append((i+1, accumulated))
    
    def point_on_path(path, segments, segment_lengths, path_lookup, dist):
        # Binary search to find the right segment
        left, right = 0, len(path_lookup) - 1
        while left < right:
            mid = (left + right) // 2
            if path_lookup[mid][1] < dist:
                left = mid + 1
            else:
                right = mid
        
        segment_idx = path_lookup[max(0, left - 1)][0]
        
        # If we're at the end of the path, return the last point
        if segment_idx >= len(segments):
            return path[-1]
        
        # Calculate how far along the segment to place the point
        dist_into_segment = dist - path_lookup[segment_idx][1]
        p1, p2 = segments[segment_idx]
        segment_length = segment_lengths[segment_idx]
        
        if segment_length == 0:  # Handle zero-length segments
            return p1
        
        # Linear interpolation
        proportion = dist_into_segment / segment_length
        return p1 + (p2 - p1) * proportion

    # Use vectorized operations and early stopping
    squared_radius = robot_radius * robot_radius  # Avoid sqrt in distance comparisons
    steps = int(max_dist / step_dist)
    
    # Check collision every n steps first for early detection of potential collisions
    check_interval = max(1, min(10, steps // 20))
    
    # First pass: Check at intervals to quickly identify potential collision regions
    for i in range(0, steps, check_interval):
        dist = i * step_dist
        point1 = point_on_path(path1, segments1, segment_lengths1, path1_lookup, dist)
        point2 = point_on_path(path2, segments2, segment_lengths2, path2_lookup, dist)
        
        # Use squared distance to avoid sqrt
        squared_dist = numpy.sum((point1 - point2) ** 2)
        
        if squared_dist < squared_radius:
            # Potential collision found, now check more precisely in this region
            start_step = max(0, i - check_interval)
            end_step = min(steps, i + check_interval)
            
            for j in range(start_step, end_step):
                precise_dist = j * step_dist
                precise_point1 = point_on_path(path1, segments1, segment_lengths1, path1_lookup, precise_dist)
                precise_point2 = point_on_path(path2, segments2, segment_lengths2, path2_lookup, precise_dist)
                
                precise_squared_dist = numpy.sum((precise_point1 - precise_point2) ** 2)
                
                if precise_squared_dist < squared_radius:
                    return precise_point1, precise_point2, j * step_dist
    
    # If no collision found after interval checks, do a more comprehensive scan
    for i in range(steps):
        if i % check_interval == 0:  # Skip steps we already checked
            continue
            
        dist = i * step_dist
        point1 = point_on_path(path1, segments1, segment_lengths1, path1_lookup, dist)
        point2 = point_on_path(path2, segments2, segment_lengths2, path2_lookup, dist)
        
        squared_dist = numpy.sum((point1 - point2) ** 2)
        
        if squared_dist < squared_radius:
            return point1, point2, i * step_dist
    
    return None


def find_waiting_point(path1, path2, step_dist=0.1, robot_radius=AGENT_RADIUS_REAL):
    """
    Find a point on path1 where the robot can wait for path2 to pass.
    """

    robot_radius *= 1.5

    def cut_path(path, dist):
        out_path = []
        dist_left = dist
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]

            segment_length = numpy.linalg.norm(p2 - p1)

            if dist_left < segment_length:
                out_path.append(p1 + (p2 - p1) * (dist_left / segment_length))
                return out_path

            dist_left -= segment_length
            out_path.append(p1)
    
        return out_path
    
    # Check if there's a collision
    collides = find_collision(path1, path2, step_dist, robot_radius)
    if collides is None:
        # print("No collision detected")
        return None
    
    point1, point2, collision_dist = collides
    
    # print(f"Collision detected at distance {collision_dist} between {point1} and {point2}")

    n_steps = int(collision_dist / step_dist)

    for i in range(n_steps, -1 , -1):
        dist = i * step_dist
        shortened_path1 = cut_path(path1, dist)

        # print(f"Shortened path waiting at: {shortened_path1[-1]} dist {dist}")

        collides = find_collision(shortened_path1, path2, step_dist, robot_radius)
        if collides is None:
            # print(f"Waiting point found at distance {dist} between {shortened_path1[-1]} and {point2}")
            return shortened_path1, point2, dist
        

    # print("No waiting point found")
    
    return None 

if __name__ == "__main__":
    # start_time = time.time()
    # generate_navmesh(
    #     input_file="polygons.txt",
    #     output_file="navmesh.txt"
    # )

    # print(f"Navmesh generation took {time.time() - start_time:.2f} seconds")
    # start_time = time.time()

    navmesh_file = "navmesh_raw.txt"

    vertices, polygons = pf.read_from_text(navmesh_file)

    sl1 = find_path(
        start=(200, 0, 270), 
        end=(800, 0, 370),
        vertices=vertices,
        polygons=polygons
    )

    sl2 = find_path(
        # start=(900, 0, 200), 
        # end=(350, 0, 350),
        start=(800, 0, 370),
        end=(200, 0, 270), 
        vertices=vertices,
        polygons=polygons
    )

    paths = find_path_two_bots(
        start1=(900, 0, 200), 
        end1=(350, 0, 350),
        start2=(800, 0, 370),
        end2=(200, 0, 270), 
        vertices=vertices,
        polygons=polygons
    )

    sl1 = paths[0]
    sl2 = paths[1]

    print("Path 1:", sl1)
    print("Path 2:", sl2)

    # collision = find_collision(sl1, sl2, step_dist=0.1, robot_radius=2)
    # if collision:
    #     point1, point2, dist = collision
    #     print(f"Collision detected between {point1} and {point2} with distance {dist}")
    # else:
    #     print("No collision detected")

    w = find_waiting_point(sl1, sl2, step_dist=1, robot_radius=0.45 * SCALE)
    if w:
        point1, point2, dist = w
        print(f"Waiting point found between {point1} and {point2} with distance {dist}")
    else:
        print("No waiting point found")