variable "ACCESS_KEY" {
    type = string
}
variable "SECRET_ACCESS_KEY" {
    type = string
}
variable "AWS_REGION" {
    type = string
    default = "eu-west-2"
}
variable "DB_HOST" {type = string}
variable "DB_NAME" {type = string}
variable "DB_PASSWORD" {type = string}
variable "DB_PORT" {type = string}
variable "DB_SCHEMA" {type = string}
variable "DB_USER" {type = string}
variable "PIPELINE_URI" {type = string}
variable "TRANSLOCATION_URI" {type = string}
variable "DASHBOARD_URI" {type = string}