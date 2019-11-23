# constants
from UtilityFunctions import resource_path, getIP

WINDOW_SIZE = 400, 200
WINDOW_NAME = 'FFS - File Sharing System'
RES_BUTTON_UPLOAD = resource_path('res/uploadButtonTexture.png')
RES_BUTTON_DOWNLOAD = resource_path('res/downloadButtonTexture.png')
RES_BUTTON_UPLOAD_HOVERED = resource_path('res/uploadButtonTextureHovered.png')
RES_BUTTON_DOWNLOAD_HOVERED = resource_path('res/downloadButtonTextureHovered.png')
RES_BUTTON_SETTINGS = resource_path('res/settingsIcon.png')
RES_BUTTON_SETTINGS_HOVERED = resource_path('res/settingsIconHovered.png')
RES_DB_SETTINGS = resource_path('res\\settings.txt')
RES_SOCKET_PORT = 9999
VERSION = 'v0.9'

# variables
isDebugEnabled = False
savePath = ''
myIP = getIP()
isLegacyMode = False
