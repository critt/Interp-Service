provider "google" {
  project = "your-gcp-project-id"
  region  = "us-west1"
}

resource "google_container_cluster" "primary" {
  name     = "interp-cluster"
  location = "us-west1"
  initial_node_count = 3
}

resource "kubernetes_deployment" "app_a" {
  metadata {
    name = "app-a"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "app-a"
      }
    }
    template {
      metadata {
        labels = {
          app = "app-a"
        }
      }
      spec {
        container {
          image = "app-a:latest"
          name  = "app-a"
          ports {
            container_port = 8080
          }
        }
      }
    }
  }
}

resource "kubernetes_deployment" "app_b" {
  metadata {
    name = "app-b"
  }
  spec {
    replicas = 3
    selector {
      match_labels = {
        app = "app-b"
      }
    }
    template {
      metadata {
        labels = {
          app = "app-b"
        }
      }
      spec {
        container {
          image = "app-b:latest"
          name  = "app-b"
          ports {
            container_port = 8080
          }
        }
      }
    }
  }
}
