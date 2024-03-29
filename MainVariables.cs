﻿using System;

namespace RobloxTweaker
{
    internal class MainVariables
    {
        public static readonly string ROBLOX_VERSIONS_DIR = Environment.GetEnvironmentVariable("LOCALAPPDATA") + "\\Roblox\\Versions";
        public static string ROBLOX_VERSION_DIR = "None";
        public static string ROBLOX_VERSION_DIR_TYPE = "None";
        public const string SETTINGS_FILE = ".\\settings.txt";
        public const string CUSTOM_TEXTURES_DIR = ".\\custom_textures";
        public const string CUSTOM_TEXTURES_TARGET_FILE = "\\target.txt";

        public static string ROBLOX_TEXTURES_DIR = "None";
        public const string PATH_TO_TEXTURES_DIR = "\\PlatformContent\\pc\\textures";
        public static string ROBLOX_CONTENT_DIR = "None";
        public const string PATH_TO_CONTENT_DIR = "\\content";
        public static readonly string[] EXCEPTION_TEXTURES = { "sky", "brdfLUT.dds", "studs.dds", "wangIndex.dds" };

        public const string BACKUP_TEXTURE_FILE = ".\\textures_backup.zip";

        public const string NEW_VERSION_SETUP_FILE = ".\\NewVersionSetup.exe";
    }
}
