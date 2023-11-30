variable "cloud_id" {
  type        = string
  description = "Yandex cloud id"
}

variable "folder_id" {
  type        = string
  description = "Yandex cloud folder id"
}

variable "sa_id" {
  type        = string
  description = "Yandex cloud service account id"
}

variable "tg_key" {
  type        = string
  description = "Telegram bot key"
}

variable "photos_bucket_name" {
  type        = string
  description = "Yandex storage photos bucket name"
  default     = "vvot28-photo"
}

variable "faces_bucket_name" {
  type        = string
  description = "Yandex storage faces bucket name"
  default     = "vvot28-faces"
}

variable "face-cut-task-queue-name" {
  type        = string
  description = "Yandex message queue name for face cut task"
  default     = "vvot28-task"
}

variable "ydb-name" {
  type        = string
  description = "YDB name"
  default     = "vvot28-db-photo-face"
}

variable "api-gateway-name" {
  type        = string
  description = "Yandex api gateway name"
  default     = "vvot28-apigw"
}

variable "face-detection-func-name" {
  type        = string
  description = "Face detection function name"
  default     = "vvot28-face-detection"
}

variable "upload-photo-trigger-name" {
  type        = string
  description = "Upload photo trigger name"
  default     = "vvot28-photo"
}

variable "face-cut-func-name" {
  type        = string
  description = "Face cut function name"
  default     = "vvot28-face-cut"
}

variable "face-cut-task-queue-trigger-name" {
  type        = string
  description = "Face cut task queue trigger name"
  default     = "vvot28-task"
}

variable "telegram-bot-func-name" {
  type        = string
  description = "Telegram bot function name"
  default     = "vvot28-telegram-bot"
}
