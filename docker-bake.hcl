# docker-bake.hcl
group "default" {
  targets = ["agent"]
}

target "agent" {
  context = "."
  dockerfile = "Dockerfile"
  tags = ["robotcontroller-agent:latest"]
}
