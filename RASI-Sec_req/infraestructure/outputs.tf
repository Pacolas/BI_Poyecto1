output "web_server_private_ip" {
  value = [
    google_compute_instance.web_server.network_interface.0.network_ip,
  ]
  description = "Web server private instance ip(They are ephemeral)"
  sensitive   = false
}

output "web_server_private_ip" {
  value = [
    google_compute_instance.db_server.network_interface.0.network_ip
  ]
  description = "DB private instance ip(They are ephemeral)"
  sensitive   = false
}
