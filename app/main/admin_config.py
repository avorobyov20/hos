"""
Настройка админки
"""
import logging
from typing import Dict

import toml

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django.urls import path


class CustomAdmin(admin.AdminSite):
    site_header = f"Hearts of Space clone - {settings.HOST_NAME}"
    index_title = f"Администрирование {settings.SERVICE_NAME}"

    def __init__(self, *args, **kwargs):
        self.version_file = "version.toml"
        self.changelog_file = "CHANGELOG.md"
        super().__init__(*args, **kwargs)

    def get_versions(self) -> Dict:
        """Получение информации о версии релиза"""
        try:
            return toml.load(self.version_file)
        except (toml.TomlDecodeError, FileNotFoundError) as error:
            logging.error(
                "Ошибка при загрузке файла %s: %s", self.version_file, error
            )
            return {}

    def each_context(self, request):
        site_data = super().each_context(request)
        release_data = self.get_versions()
        return {
            **site_data,
            "version": release_data.get("version"),
            "release_url": release_data.get("release_url"),
            "release_date": release_data.get("release_date"),
        }

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path("release/", self.admin_view(self.changelog), name="release")
        ]
        return custom_urls + urls

    def changelog(self, request: HttpRequest) -> TemplateResponse:

        try:
            with open(self.changelog_file, "r", encoding="utf-8") as file:
                changelog = file.read()
        except (FileNotFoundError, UnicodeEncodeError) as error:
            logging.error(
                "Ошибка при загрузке файла %s: %s", self.changelog_file, error
            )
            changelog = "Ошибка при загрузке истории изменений"

        context = dict(self.each_context(request), changelog=changelog)
        return TemplateResponse(request, "admin/changelog.html", context)


class MainAdminConfig(AdminConfig):
    """Переопределение класса админки"""

    default_site = "main.admin_config.CustomAdmin"
