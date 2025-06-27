terraform {
  required_providers {
    okta = {
      source  = "okta/okta"
      version = "~> 4.0"
    }
  }
}

provider "okta" {
  org_name  = "dev-47311371"    # <--- Your Okta subdomain here
  base_url  = "okta.com"
  api_token = var.okta_api_token
}

# Groups
resource "okta_group" "admins" {
  name        = "admins"
  description = "Admin users"
}

resource "okta_group" "regulars" {
  name        = "regular-users"
  description = "Regular access users"
}

# Users
resource "okta_user" "admin_user" {
  first_name = "Kamaal"
  last_name  = "Admin"
  email      = "kamaalm001@gmail.com"
  login      = "kamaalm001@gmail.com"
  password   = "SuperSecure1!"    # Okta requires strong passwords
}

resource "okta_user" "regular_user" {
  first_name = "Meerzah"
  last_name  = "Regular"
  email      = "kamaal987+1@gmail.com"
  login      = "kamaal987+1@gmail.com"
  password   = "SuperSecure2!"
}

# Group Memberships
resource "okta_user_group_memberships" "admin_membership" {
  user_id = okta_user.admin_user.id
  groups  = [okta_group.admins.id]
}

resource "okta_user_group_memberships" "regular_membership" {
  user_id = okta_user.regular_user.id
  groups  = [okta_group.regulars.id]
}

 # OIDC App (assumes you already created one in Okta manually)
data "okta_app_oauth" "flask_app" {
  label = "IAM Flask API"   # <--- Must match app name in Okta UI
}

resource "okta_app_group_assignment" "assign_admins" {
 app_id    =   data.okta_app_oauth.flask_app.id
group_id  =   okta_group.admins.id
}

#resource "okta_app_group_assignment" "assign_regulars" {
 # app_id    =   data.okta_app_oauth.flask_app.id
  #group_id  =   okta_group.regulars.id
#}
