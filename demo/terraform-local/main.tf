# DEMO 4 - a first look at Terraform, with no cloud account needed.
#
# The "local" provider manages files on disk the same way the azurerm
# provider manages Azure resources: you declare them, Terraform plans,
# applies, records them in a state file, and detects drift.
#
#   terraform init
#   terraform plan
#   terraform apply        # type "yes"
#   terraform apply        # run again: "No changes."
#   echo "hacked" > out/web-1.conf ; terraform plan   # drift!
#   terraform destroy

terraform {
  required_version = ">= 1.6"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

variable "vms" {
  description = "VMs we want, and their size."
  type        = map(string)
  default = {
    "web-1" = "small"
    "web-2" = "small"
  }
}

resource "local_file" "vm" {
  for_each = var.vms

  filename = "${path.module}/out/${each.key}.conf"
  content  = "name=${each.key}\nsize=${each.value}\n"
}

output "vm_files" {
  value = [for f in local_file.vm : f.filename]
}
