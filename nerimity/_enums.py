import datetime

class GlobalClientInformation():
    TOKEN = ''
    SERVERS = {}
    BUTTONS = []
    API_URL = 'https://nerimity.com/api'
    CDN_URL = 'https://cdn.nerimity.com'
    WEBSOCKET_URL = 'wss://nerimity.com'

class ConsoleShortcuts():
    @staticmethod
    def log():   return f"{Colors.MAGENTA}[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}]{Colors.WHITE} |"
    @staticmethod
    def ok():    return f"{Colors.GREEN}[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}]{Colors.WHITE} |"
    @staticmethod
    def warn():  return f"{Colors.YELLOW}[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}]{Colors.WHITE} |"
    @staticmethod
    def error(): return f"{Colors.RED}[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}]{Colors.WHITE} |"

class Colors():
    BLACK = "\u001b[30m"
    RED = "\u001b[31m"
    GREEN = "\u001b[32m"
    YELLOW = "\u001b[33m"
    BLUE = "\u001b[34m"
    MAGENTA = "\u001b[35m"
    CYAN = "\u001b[36m"
    WHITE = "\u001b[37m"

class ChannelTypes():
    DM_TEXT = 0
    SERVER_TEXT = 1
    CATEGORY = 2

class PresenceTypes():
    OFFLINE = 0
    ONLINE = 1
    LTP = 2
    AFK = 3
    DND = 4

class BadgeTypes():
    OWNER = 1
    ADMIN = 2
    CONTRIBUTOR = 4
    SUPPORTER = 8
    BOT = 16

class MessageType():
    CONTENT = 0
    JOIN_SERVER = 1
    LEAVE_SERVER = 2
    KICK_USER = 3
    BAN_USER = 4
    CALL_STARTED = 5

class AttachmentTypes():
    INCOMING = 0
    OUTGOING = 1

class EmbedTypes():
    HTML = 0

class Permissions:
    """ Permissions class """
    class ChannelPermissions():
        """
        Channel Permissions class 
        
        # Attributes
        public: bool - Whether the channel is public or not
        send_messages: bool - Whether the user can send messages or not
        join_voice: bool - Whether the user can join voice channels or not

        """
        def __init__(self):
            """
            Initialize the ChannelPermissions object.

            Args:
                public (bool): Indicates if the channel is public.
                send_messages (bool): Indicates if sending messages is allowed.
                join_voice (bool): Indicates if joining voice is allowed.

            Returns:
                int: The permission integer.
            """
            self.public = None
            self.send_messages = None
            self.join_voice = None
            self.permission_integer = 0
        

        def from_integer(self, integer: int) -> 'Permissions.ChannelPermissions':
            """
            Initialize the ChannelPermissions object from an integer.

            Args:
                integer (int): The permission integer.

            Returns:
                ChannelPermissions: The ChannelPermissions object.
            """
            self.public = bool(integer & 1)
            self.send_messages = bool(integer & 2)
            self.join_voice = bool(integer & 4)
            self.permission_integer = integer
            return self
        
        @staticmethod
        def construct(public: bool, send_messages: bool, join_voice: bool) -> int:
            """
            Construct the ChannelPermissions object.

            Args:
            public (bool): Indicates if the channel is public.
            send_messages (bool): Indicates if sending messages is allowed.
            join_voice (bool): Indicates if joining voice is allowed.

            Returns:
            int: The permission integer.
            """
            instance = Permissions.ChannelPermissions()
            instance.public = public
            instance.send_messages = send_messages
            instance.join_voice = join_voice
            return instance.__calculate_permissions()

        
        # Private: calculates the permissions
        def __calculate_permissions(self) -> int:
            if self.public:
                self.permission_integer += 1
            if self.send_messages:
                self.permission_integer += 2
            if self.join_voice:
                self.permission_integer += 4
            return self.permission_integer

    class RolePermissions():
        """
        Role Permissions class

        # Attributes
        admin: bool - Whether the role is an admin or not
        send_messages: bool - Whether the role can send messages or not
        manage_roles: bool - Whether the role can manage roles or not
        manage_channels: bool - Whether the role can manage channels or not
        kick: bool - Whether the role can kick users or not
        ban: bool - Whether the role can ban users or not
        mention_everyone: bool - Whether the role can mention everyone or not
        nickname_member: bool - Whether the role can change nicknames or not
        mention_roles: bool - Whether the role can mention roles or not
        """

        def __init__(self) -> None:
            """
            Initialize the RolePermissions object.

            Args:
                None

            Returns:
                None
            """
            self.admin = None
            self.send_messages = None
            self.manage_roles = None
            self.manage_channels = None
            self.kick = None
            self.ban = None
            self.mention_everyone = None
            self.nickname_member = None
            self.mention_roles = None
            self.permission_integer = 0
        
        @property
        def from_integer(self, integer: int) -> 'Permissions.RolePermissions':
            """
            Initialize the RolePermissions object from an integer.

            Args:
                integer (int): The permission integer.

            Returns:
                RolePermissions: The RolePermissions object.
            """
            self.admin = bool(integer & 1)
            self.send_messages = bool(integer & 2)
            self.manage_roles = bool(integer & 4)
            self.manage_channels = bool(integer & 8)
            self.kick = bool(integer & 16)
            self.ban = bool(integer & 32)
            self.mention_everyone = bool(integer & 64)
            self.nickname_member = bool(integer & 128)
            self.mention_roles = bool(integer & 256)
            self.permission_integer = integer
            return self
        

        @staticmethod
        def construct(admin: bool = False, send_messages: bool = False, manage_roles: bool = False, manage_channels: bool = False, 
                      kick: bool = False, ban: bool = False, mention_everyone: bool = False, nickname_member: bool = False, mention_roles: bool = False) -> int:
            """
            Construct the RolePermissions object.

            Args:
                admin (bool): Indicates if the role is an admin.
                send_messages (bool): Indicates if sending messages is allowed.
                manage_roles (bool): Indicates if managing roles is allowed.
                manage_channels (bool): Indicates if managing channels is allowed.
                kick (bool): Indicates if kicking is allowed.
                ban (bool): Indicates if banning is allowed.
                mention_everyone (bool): Indicates if mentioning everyone is allowed.
                nickname_member (bool): Indicates if changing nicknames is allowed.
                mention_roles (bool): Indicates if mentioning roles is allowed.

            Returns:
                RolePermissions: The RolePermissions object.
            """
            instance = Permissions.RolePermissions()
            instance.admin = admin
            instance.send_messages = send_messages
            instance.manage_roles = manage_roles
            instance.manage_channels = manage_channels
            instance.kick = kick
            instance.ban = ban
            instance.mention_everyone = mention_everyone
            instance.nickname_member = nickname_member
            instance.mention_roles = mention_roles
            return instance.__calculate_permissions()
        
        # Private: calculates the permissions
        def __calculate_permissions(self) -> int:
            if self.admin:
                self.permission_integer += 1
            if self.send_messages:
                self.permission_integer += 2
            if self.manage_roles:
                self.permission_integer += 4
            if self.manage_channels:
                self.permission_integer += 8
            if self.kick:
                self.permission_integer += 16
            if self.ban:
                self.permission_integer += 32
            if self.mention_everyone:
                self.permission_integer += 64
            if self.nickname_member:
                self.permission_integer += 128
            if self.mention_roles:
                self.permission_integer += 256
            return self.permission_integer
