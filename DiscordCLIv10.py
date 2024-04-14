import configparser
import requests
import random
import psutil
import json
import sys
import os

help_message = """
General:
    exit
    clear
    help
    settings
    set user token <value> / set tor <host/port_range> <value>

Channel:
    # GET
    get_channel(channel_id)
    get_channel_messages(channel_id)
    get_channel_message(channel_id, message_id)
    get_reactions(channel_id, message_id, emoji)
    get_channel_invites(channel_id)
    get_pinned_messages(channel_id)
    get_thread_member(channel_id, user_id)
    list_thread_members(channel_id)
    list_public_archived_threads(channel_id)
    list_private_archived_threads(channel_id)
    list_joined_private_archived_threads(channel_id)

    # PATCH
    modify_channel(channel_id)
    edit_message(channel_id, message_id)

    # DELETE
    delete_close_channel(channel_id)
    delete_own_reaction(channel_id, message_id, emoji)
    delete_user_reaction(channel_id, message_id, emoji, user_id)
    delete_all_reactions(channel_id, message_id)
    delete_all_reactions_for_emoji(channel_id, message_id, emoji)
    delete_message(channel_id, message_id)
    bulk_delete_messages(channel_id)
    delete_channel_permissions(channel_id, overwrite_id)
    unpin_message(channel_id, message_id)
    group_dm_remove_recipient(channel_id, user_id)
    leave_thread(channel_id)
    remove_thread_member(channel_id, user_id)

    # POST
    create_message(channel_id)
    crosspost_message(channel_id, message_id)
    create_channel_invite(channel_id)
    follow_announcement_channel(channel_id)
    trigger_typing_indicator(channel_id)
    start_thread_from_message(channel_id, message_id)
    start_thread_without_message(channel_id)
    start_thread_in_forum_or_media_channel(channel_id)

    # PUT
    create_reaction(channel_id, message_id, emoji)
    edit_channel_permissions(channel_id, overwrite_id)
    pin_message(channel_id, message_id)
    group_dm_add_recipient(channel_id, user_id)
    join_thread(channel_id)
    add_thread_member(channel_id, user_id)

Emoji:
    # GET
    list_guild_emojis(guild_id)
    get_guild_emoji(guild_id, emoji_id)

    # POST
    create_guild_emoji(guild_id)

    # PATCH
    modify_guild_emoji(guild_id, emoji_id)

    # DELETE
    delete_guild_emoji(guild_id, emoji_id)

Guild:
    # POST
    create_guild()
    create_guild_channel(guild_id)
    bulk_guild_ban(guild_id)
    create_guild_role(guild_id)
    modify_guild_mfa_level(guild_id)
    begin_guild_prune(guild_id)

    # GET
    get_guild(guild_id)
    get_guild_preview(guild_id)
    get_guild_channels(guild_id)
    list_active_guild_threads(guild_id)
    get_guild_member(guild_id, user_id)
    list_guild_members(guild_id)
    search_guild_members(guild_id)
    get_guild_bans(guild_id)
    get_guild_ban(guild_id, user_id)
    get_guild_roles(guild_id)
    get_guild_prune_count(guild_id)
    get_guild_voice_regions(guild_id)
    get_guild_invites(guild_id)
    get_guild_integrations(guild_id)
    get_guild_widget_settings(guild_id)
    get_guild_widget(guild_id)
    get_guild_vanity_url(guild_id)
    get_guild_widget_image(guild_id)
    get_guild_welcome_screen(guild_id)
    get_guild_onboarding(guild_id)

    # PATCH
    modify_guild(guild_id)
    modify_guild_channel_positions(guild_id)
    modify_guild_member(guild_id, user_id)
    modify_current_member(guild_id)
    modify_current_user_nick(guild_id)
    modify_guild_role_position(guild_id)
    modify_guild_role(guild_id, user_id)
    modify_guild_widget(guild_id)
    modify_guild_welcome_screen(guild_id)
    modify_current_user_voice_state(guild_id)
    modify_user_voice_state(guild_id, user_id)

    # DELETE
    delete_guild(guild_id)
    remove_guild_member_role(guild_id, user_id, role_id)
    remove_guild_member(guild_id, user_id)
    remove_guild_ban(guild_id, user_id)
    delete_guild_role(guild_id, role_id)
    delete_guild_integration(guild_id, integration_id)

    # PUT
    add_guild_member(guild_id, user_id)
    add_guild_member_role(guild_id, user_id, role_id)
    create_guild_ban(guild_id, user_id)
    modify_guild_onboarding(guild_id)

GuildScheduldedEvent:
    # POST
    create_guild_scheduled_event(guild_id)

    # GET
    get_guild_scheduled_event(guild_id, guild_scheduled_event_id)
    get_guild_scheduled_event_users(guild_id, guild_scheduled_event_id)

    # PATCH
    modify_guild_scheduled_event(guild_id, guild_scheduled_event_id)

    # DELETE
    delete_guild_scheduled_event(guild_id, guild_scheduled_event_id)

GuildTemplate:
    # GET
    get_guild_template(template_code)
    get_guild_templates(guild_id)

    # POST
    create_guild_from_guild_template(template_code)
    create_guild_template(guild_id)

    # PUT
    sync_guild_template(guild_id, template_code)

    # PATCH
    modify_guild_template(guild_id, template_code)

    # DELETE
    delete_guild_template(guild_id, template_code)

Invite:
    # GET
    get_invite(invite_code)

    # DELETE
    delete_invite(invite_code)

StageInstance:
    # POST
    create_stage_instance()

    # GET
    get_stage_instance(channel_id)

    # PATCH
    modify_stage_instance(channel_id)

    # DELETE
    delete_stage_instance(channel_id)

Sticker:
    # GET
    get_sticker(sticker_id)
    list_sticker_packs()
    list_guild_stickers(guild_id)
    get_guild_sticker(guild_id, sticker_id)

    # POST
    create_guild_sticker(guild_id)

    # PATCH
    modify_guild_sticker(guild_id, sticker_id)

    # DELETE
    delete_guild_sticker(guild_id, sticker_id)

User:
    # GET
    get_current_user()
    get_user(user_id)
    get_current_user_guilds()
    get_current_user_guild_member(guild_id)
    get_current_user_connections()
    get_current_user_application_role_connection(application_id)

    # PATCH
    modify_current_user(username, avatar)

    # DELETE
    leave_guild(guild_id)

    # POST
    create_dm(recipient_id)
    create_group_dm(access_tokens, nicks)

    # PUT
    update_current_user_application_role_connection(application_id)

Voice:
    # GET
    list_voice_regions()

Webhook:
    # GET
    get_channel_webhooks(guild_id)
    get_webhook(webhook_id)
    get_webhook_with_token(webhook_id, webhook_token)
    get_webhook_message(webhook_id, webhook_token, message_id)

    # PATCH
    modify_webhook(webhook_id)
    modify_webhook_with_token(webhook_id, webhook_token)
    edit_webhook_message(webhook_id, webhook_token, message_id)

    # DELETE
    delete_webhook(webhook_id)
    delete_webhook_with_token(webhook_id, webhook_token)
    delete_webhook_message(webhook_id, webhook_token, message_id)

    # POST
    execute_webhook(webhook_id, webhook_token)
    execute_slack_compatible_webhook(webhook_id, webhook_token)
    execute_github_compatible_webhook(webhook_id, webhook_token)
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def fetch_data(url, method=None, params=None, data=None, headers=None, cookies=None, files=None, auth=None, timeout=None, allow_redirects=None, proxies=None, hooks=None, stream=None, verify=None, cert=None, json=None):
    try:
        if method == "get":
            response = requests.get(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        elif method == "patch":
            response = requests.patch(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        elif method == "delete":
            response = requests.delete(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        elif method == "post":
            response = requests.post(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        elif method == "put":
            response = requests.put(url, params=params, data=data, headers=headers, cookies=cookies, files=files, auth=auth, timeout=timeout, allow_redirects=allow_redirects, proxies=proxies, hooks=hooks, stream=stream, verify=verify, cert=cert, json=json)
        
        try:
            if response.text:
                return response.json()
            else:
                return {"response": response.status_code}
        except:
            return {"error": response.text}
    except Exception as e:
        return {"error": str(e)}
    
class Tor:
    def configure():
        try:
            path = "tor\\torrc"
            ports = range(port1, port2)

            with open(path, "w") as torrc_file:
                for port in ports:
                    line = f"SocksPort {host}:{port}\n"
                    torrc_file.write(line)
            return True
        except Exception as e:
            return e
        
    def start():
        Tor.stop()
        Tor.configure()

        os.system("start tor\\tor.exe -f tor\\torrc")

    def stop():
        for proc in psutil.process_iter(['pid', 'name']):
            if "tor.exe" == proc.info['name'].lower() or "tor" == proc.info['name'].lower():
                proc.kill()

class DiscordApi:
    version_number = 10
    base_url = "https://discord.com/api"
    url = f"https://discord.com/api/v{version_number}"

    class Channel:
        # GET
        def get_channel(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_channel_messages(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages?limit=100"
            query_string_params = ['around?', 'before?', 'ater?', 'limit?']

        def get_channel_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}"

        def get_reactions(channel_id, message_id, emoji):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
            query_string_params = ['after?', 'limit?']

        def get_channel_invites(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/invites"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_pinned_messages(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/pins"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_thread_member(channel_id, user_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/thread-members/{user_id}"
            query_string_params = ['with_member?']

        def list_thread_members(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/thread-members"
            query_string_params = ['with_member?', 'after?', 'limit?']

        def list_public_archived_threads(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/threads/archived/public"
            query_string_params = ['after?', 'limit?']
            response_body = ['threads', 'members', 'has_more']

        def list_private_archived_threads(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/threads/archived/private"
            query_string_params = ['after?', 'limit?']
            response_body = ['threads', 'members', 'has_more']

        def list_joined_private_archived_threads(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/users/@me/threads/archived/private"
            query_string_params = ['after?', 'limit?']
            response_body = ['threads', 'members', 'has_more']

        # PATCH
        def modify_channel(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}"
            json_params_group_dm = ['name', 'icon']
            json_paramgs_guild_channel = ['name', 'type', 'position', 'topic', 'nsfw', 'rate_limit_per_user', 'bitrate*', 'user_limit', 'permission_overwrites**', 'parent_id', 'rtc_region', 'video_quality_mode',
                                          'default_auto_archive_duration', 'flags?', 'available_tags?', 'default_reaction_emoji?', 'default_thread_rate_limit_per_user?', 'default_sort_order?', 'default_forum_layout?']
            json_params_thread = ['name', 'archived', 'auto_archive_duration', 'locked', 'invitable', 'rate_limit_per_user', 'flags?', 'applied_tags?']

        def edit_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}"
            json_form_params = ['content', 'embeds', 'flags', 'allowed_mentions', 'components', 'files[n]', 'payload_json', 'attachments']

        # DELETE
        def delete_close_channel(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def delete_own_reaction(channel_id, message_id, emoji):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def delete_user_reaction(channel_id, message_id, emoji, user_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data
        
        def delete_all_reactions(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/reactions"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def delete_all_reactions_for_emoji(channel_id, message_id, emoji):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data
        
        def delete_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def bulk_delete_messages(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/bulk-delete"
            json_params = ['messages 2-100']

        def delete_channel_permissions(channel_id, overwrite_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/permissions/{overwrite_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def unpin_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/pins/{message_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def group_dm_remove_recipient(channel_id, user_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/recipients/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def leave_thread(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/thread-members/@me"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def remove_thread_member(channel_id, user_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/thread-members/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # POST
        def create_message(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages"
            json_form_params = ['content?*', 'nonce?', 'tts?', 'embeds?*', 'allowed_mentions?', 'message_reference?', 'components?*',
                                'sticker_ids?*', 'files[n]?*', 'payload_json?', 'attachments?', 'flags?', 'enforce_nonce?']
        
        def crosspost_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/crosspost"

        def create_channel_invite(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/invites"
            json_params = ['max_age', 'max_uses', 'temporary', 'unique', 'target_type', 'target_user_id', 'target_application_id']
        
        def follow_announcement_channel(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/followers"
            json_params = ['webhook_channel_id']

        def trigger_typing_indicator(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/typing"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="post", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def start_thread_from_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/threads"
            json_params = ['name', 'auto_archive_duration?', 'rate_limit_per_user?']

        def start_thread_without_message(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/threads"
            json_params = ['name', 'auto_archive_duration?', 'type?*', 'invitable?', 'rate_limit_per_user?']

        def start_thread_in_forum_or_media_channel(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/threads"
            json_form_params = ['name', 'auto_archive_duration?*', 'rate_limit_per_user?', 'message', 'applied_tags?', 'files[n]?*', 'payload_json?']
            forum_and_media_thread_message_params_object = ['content?*', 'embed?*', 'allowed_mentions?', 'components?*', 'sticker_ids?*', 'attachments?', 'flags?']
        
        # PUT
        def create_reaction(channel_id, message_id, emoji):
            url = f"{DiscordApi.url}/channels/{channel_id}/messages/{message_id}/reactions/{emoji}/@me"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def edit_channel_permissions(channel_id, overwrite_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/permissions/{overwrite_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def pin_message(channel_id, message_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/pins/{message_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def group_dm_add_recipient(channel_id, user_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/recipients/{user_id}"
            json_params = ['access_token', 'nick']

        def join_thread(channel_id):
            url = f"{DiscordApi.utl}/channels/{channel_id}/thread-members/@me"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def add_thread_member(channel_id, user_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/thread-members/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class Emoji:
        # GET
        def list_guild_emojis(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/emojis"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_emoji(guild_id, emoji_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/emojis/{emoji_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # POST
        def create_guild_emoji(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/emojis"
            json_params = ['name', 'image', 'roles']

        # PATCH
        def modify_guild_emoji(guild_id, emoji_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/emojis/{emoji_id}"
            json_params = ['image', 'roles']

        # DELETE
        def delete_guild_emoji(guild_id, emoji_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/emojis/{emoji_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class Guild:
        # POST
        def create_guild():
            url = f"{DiscordApi.url}/guilds"
            json_params = ['name', 'region?', 'icon?', 'verification_level?', 'default_message_notifications?', 'explicit_content_filter?',
                           'roles?', 'channels?', 'afk_channel_id?', 'afk_timeout?', 'system_channel_id?', 'system_channel_flags?']

        def cerate_guild_channel(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/channels"
            json_params = ['name', 'type', 'topic', 'bitrate*', 'user_limit', 'rate_limit_per_user', 'position', 'permission_overwrites**', 'parent_id', 'nsfw', 'rtc_region', 'video_quality_mode',
                           'default_auto_archive_duration', 'default_reaction_emoji', 'available_tags', 'default_sort_order', 'default_forum_layout', 'default_forum_layout', 'default_thread_rate_limit_per_user']
        
        def bulk_guild_ban(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/bulk-ban"
            json_params = ['user_ids', 'delete_message_seconds?']
            bulk_ban_response = ['banned_users', 'failed_users']

        def create_guild_role(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/roles"
            json_params = ['name', 'permissions', 'color', 'hoist', 'icon', 'unicode_emoji', 'mentionable']

        def modify_guild_mfa_level(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/mfa"
            json_params = ['level']

        def begin_guild_prune(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/prune"
            json_params = ['days', 'compute_prune_count', 'include_roles', 'reason?']

        # GET
        def get_guild(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}?with_counts=True"
            query_string_params = ['with_counts?']

        def get_guild_preview(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/preview"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_channels(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/channels"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def list_active_guild_threads(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/threads/active"
            response_body = ['threads', 'members']

        def get_guild_member(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def list_guild_members(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members?limit=1000"
            query_string_params = ['limit', 'after']

        def search_guild_members(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/search?limit=1000"
            query_string_params = ['query', 'limit']

        def get_guild_bans(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/bans"
            query_string_params = ['limit?', 'before?*', 'after?*']

        def get_guild_ban(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/bans/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_roles(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/roles"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_prune_count(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/prune"
            query_string_params = ['days', 'include_roles']

        def get_guild_voice_regions(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/regions"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_invites(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/invites"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_integrations(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/integrations"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_widget_settings(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/widget"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_widget(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/widget.json"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_vanity_url(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/vanity-url"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_widget_image(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/widget.png"
            query_string_params = ['style']
            widget_style_options = ['shield', 'banner1', 'banner2', 'banner3', 'banner4']

        def get_guild_welcome_screen(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/welcome-screen"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_onboarding(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/onboarding"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # PATCH
        def modify_guild(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}"
            json_params = ['name', 'region', 'verification_level', 'default_message_notifications', 'explicit_content_filter', 'afk_channel_id', 'afk_timeout', 'icon', 'owner_id', 'splash', 'discovery_splash', 'banner',
                           'system_channel_id', 'system_channel_flags', 'rules_channel_id', 'public_updates_channel_id', 'preferred_locale', 'features', 'description', 'premium_progress_bar_enabled', 'safety_alerts_channel_id']
        
        def modify_guild_channel_positions(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/channels"
            json_params = ['id', 'position?', 'lock_permissions?', 'parent_id?']

        def modify_guild_member(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/{user_id}"
            json_params = ['nick', 'roles', 'mute', 'deaf', 'channel_id', 'communication_disabled_until', 'flags']

        def modify_current_member(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/@me"
            json_params = ['nick?']

        def modify_current_user_nick(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/@me/nick"
            json_params = ['nick?']

        def modify_guild_role_position(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/roles"
            json_params = ['id', 'position?']

        def modify_guild_role(guild_id, role_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/roles/{role_id}"
            json_params = ['name', 'permissions', 'color', 'hoist', 'icon', 'unicode_emoji', 'mentionable']

        def modify_guild_widget(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/widget"

        def modify_guild_welcome_screen(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/welcome-screen"
            json_params = ['enabled', 'welcome_channels', 'description']

        def modify_current_user_voice_state(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/voice-states/@me"
            json_params = ['channel_id?', 'suppress?', 'request_to_speak_timestamp?']

        def modify_user_voice_state(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/voice-states/{user_id}"
            json_params = ['channel_id', 'suppress?']

        # DELETE
        def delete_guild(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def remove_guild_member_role(guild_id, user_id, role_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data
            
        def remove_guild_member(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def remove_guild_ban(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/bans/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def delete_guild_role(guild_id, role_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/roles/{role_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def delete_guild_integration(guild_id, integration_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/integrations/{integration_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # PUT
        def add_guild_member(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/{user_id}"
            json_params = ['access_token', 'nick', 'roles', 'mute', 'deaf']

        def add_guild_member_role(guild_id, user_id, role_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/members/{user_id}/roles/{role_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def create_guild_ban(guild_id, user_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/bans/{user_id}"
            json_params = ['delete_message_days?', 'delete_message_seconds?']

        def modify_guild_onboarding(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/onboarding"
            json_params = ['prompts', 'default_channel_ids', 'enabled', 'mode']

    class GuildScheduldedEvent:
        # POST
        def create_guild_scheduled_event(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/scheduled-events"
            json_params = ['channel_id? *', 'entity_metadata? **', 'name', 'privacy_level', 'scheduled_start_time',
                           'scheduled_end_time? **', 'description?', 'entity_type', 'image?']
            
        # GET
        def get_guild_scheduled_event(guild_id, guild_scheduled_event_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
            query_string_params = ['with_user_count?']

        def get_guild_scheduled_event_users(guild_id, guild_scheduled_event_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
            query_string_params = ['limit?', 'with_member?', 'before? *', 'after? *']

        # PATCH
        def modify_guild_scheduled_event(guild_id, guild_scheduled_event_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
            json_params = ['channel_id? *', 'entity_metadata?', 'name?', 'privacy_level?', 'scheduled_start_time?',
                           'scheduled_end_time? *', 'description?', 'entity_type? *', 'status?', 'image?']
            
        # DELETE
        def delete_guild_scheduled_event(guild_id, guild_scheduled_event_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/scheduled-events/{guild_scheduled_event_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class GuildTemplate:
        # GET
        def get_guild_template(template_code):
            url = f"{DiscordApi.url}/guilds/templates/{template_code}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_templates(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/templates"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # POST
        def create_guild_from_guild_template(template_code):
            url = f"{DiscordApi.url}/guilds/templates/{template_code}"
            json_params = ['name', 'icon?']

        def create_guild_template(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/templates"
            json_params = ['name', 'description?']

        # PUT
        def sync_guild_template(guild_id, template_code):
            url = f"{DiscordApi.url}/guilds/{guild_id}/templates/{template_code}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="put", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # PATCH
        def modify_guild_template(guild_id, template_code):
            url = f"{DiscordApi.url}/guilds/{guild_id}/templates/{template_code}"
            json_params = ['name?', 'description?']

        # DELETE
        def delete_guild_template(guild_id, template_code):
            url = f"{DiscordApi.url}/guilds/{guild_id}/templates/{template_code}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class Invite:
        # GET
        def get_invite(invite_code):
            url = f"{DiscordApi.url}/invites/{invite_code}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # DELETE
        def delete_invite(invite_code):
            url = f"{DiscordApi.url}/invites/{invite_code}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class StageInstance:
        # POST
        def create_stage_instance():
            url = f"{DiscordApi.url}/stage-instances"
            json_params = ['channel_id', 'topic', 'privacy_level?', 'send_start_notification? *', 'guild_scheduled_event_id?']

        # GET
        def get_stage_instance(channel_id):
            url = f"{DiscordApi.url}/stage-instances/{channel_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # PATCH
        def modify_stage_instance(channel_id):
            url = f"{DiscordApi.url}/stage-instances/{channel_id}"
            json_params = ['topic?', 'privacy_level?']

        # DELETE
        def delete_stage_instance(channel_id):
            url = f"{DiscordApi.url}/stage-instances/{channel_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class Sticker:
        # GET
        def get_sticker(sticker_id):
            url = f"{DiscordApi.url}/stickers/{sticker_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def list_sticker_packs():
            url = f"{DiscordApi.url}/sticker-packs"
            response_structure = ['sticker_packs']

        def list_guild_stickers(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/stickers"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_guild_sticker(guild_id, sticker_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/stickers/{sticker_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # POST
        def create_guild_sticker(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/stickers"
            form_params = ['name', 'description', 'tags', 'file']

        # PATCH
        def modify_guild_sticker(guild_id, sticker_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/stickers/{sticker_id}"
            json_params = ['name', 'description', 'tags']

        # DELETE
        def delete_guild_sticker(guild_id, sticker_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/stickers/{sticker_id}"

    class User:
        # GET
        def get_current_user():
            url = f"{DiscordApi.url}/users/@me"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_user(user_id):
            url = f"{DiscordApi.url}/users/{user_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_current_user_guilds():
            url = f"{DiscordApi.url}/users/@me/guilds?with_counts=True"
            query_string_params = ['before', 'after', 'limit', 'with_counts']
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_current_user_guild_member(guild_id):
            url = f"{DiscordApi.url}/users/@me/guilds/{guild_id}/member"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_current_user_connections():
            url = f"{DiscordApi.url}/users/@me/connections"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_current_user_application_role_connection(application_id):
            url = f"{DiscordApi.url}/users/@me/applications/{application_id}/role-connection"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        # PATCH
        def modify_current_user(username, avatar):
            url = f"{DiscordApi.url}/users/@me"
            json_params = ['username', 'avatar']

        # DELETE
        def leave_guild(guild_id):
            url = f"{DiscordApi.url}/users/@me/guilds/{guild_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="delete", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data
            
        # POST
        def create_dm(recipient_id):
            url = f"{DiscordApi.url}/users/@me/channels"
            json_params = [recipient_id]

        def create_group_dm(access_tokens, nicks):
            url = f"{DiscordApi.url}/users/@me/channels"
            json_params = [access_tokens, nicks]

        # PUT
        def update_current_user_application_role_connection(application_id):
            url = f"{DiscordApi.url}/users/@me/applications/{application_id}/role-connection"
            json_params = ['platform_name?', 'platform_username?', 'metadata?']

    class Voice:
        # GET
        def list_voice_regions():
            url = f"{DiscordApi.url}/voice/regions"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

    class Webhook:
        # POST
        def create_webhook(channel_id):
            url = f"{DiscordApi.url}/channels/{channel_id}/webhooks"
            json_params = ['name', 'avatar?']

        # GET
        def get_channel_webhooks(guild_id):
            url = f"{DiscordApi.url}/guilds/{guild_id}/webhooks"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_webhook(webhook_id):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_webhook_with_token(webhook_id, webhook_token):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="get", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def get_webhook_message(webhook_id, webhook_token, message_id):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
            query_string_params = ['thread_id']

        # PATCH
        def modify_webhook(webhook_id):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}"
            json_params = ['name', 'avatar', 'channel_id']

        def modify_webhook_with_token(webhook_id, webhook_token):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}"
            headers = {'Authorization': user_token, 'User-Agent': random.choice(user_agents)}

            proxy = random.choice(proxies)
            proxy_dict = {'http': f'socks5h://{proxy}', 'https': f'socks5h://{proxy}'}

            data = fetch_data(url=url, method="patch", headers=headers, proxies=proxy_dict)
            print(json.dumps(data, indent=True), '\n')
            return data

        def edit_webhook_message(webhook_id, webhook_token, message_id):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
            query_string_params = ['thread_id']
            json_form_params = ['content', 'embeds', 'allowed_mentions', 'components *',
                                'files[n] **', 'payload_json **', 'attachments **']

        # DELETE
        def delete_webhook(webhook_id):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}"
            
        def delete_webhook_with_token(webhook_id, webhook_token):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}"

        def delete_webhook_message(webhook_id, webhook_token, message_id):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}/messages/{message_id}"
            query_string_params = ['thread_id']
            
        # POST
        def execute_webhook(webhook_id, webhook_token):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}"
            query_string_params = ['wait', 'thread_id']
            json_forms_params = ['content', 'username', 'avatar_url', 'tts', 'embeds', 'allowed_mentions', 'components *',
                                 'files[n] **', 'payload_json **', 'attachments **', 'flags', 'thread_name', 'applied_tags']
        
        def execute_slack_compatible_webhook(webhook_id, webhook_token):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}/slack"
            query_string_params = ['thread_id', 'wait']

        def execute_github_compatible_webhook(webhook_id, webhook_token):
            url = f"{DiscordApi.url}/webhooks/{webhook_id}/{webhook_token}/github"
            query_string_params = ['thread_id', 'wait']

    
if __name__ == "__main__":
    clear()

    config = configparser.ConfigParser()
    config.read('config.ini')

    user_token = config.get('Token', 'user')

    port_range = config.get('Tor', 'port_range')
    port1, port2 = port_range.split(',')
    port1 = int(port1)
    port2 = int(port2)

    host = config.get('Tor', 'host')
    proxies = [f"{host}:{port}" for port in range(port1, port2)]
    Tor.start()

    with open('user-agents.txt', 'r') as file:
        user_agents = [line.strip() for line in file.readlines()]

    while True:
        cmd = input("DiscordCLI$ ").split(" ")
        
        if cmd[0] == "exit":
            sys.exit()
        elif cmd[0] == "clear":
            clear()
        elif cmd[0] in ["help", "?"]:
            print(help_message)
        elif cmd[0] == "exec":
            cmd = " ".join(cmd[1:])
            try:
                exec(cmd)
            except Exception as e:
                print(e)

        elif cmd[0] == "settings":
            print(f"User token: {user_token}\n\nTor host: {host}\nTor port range: {port_range}\n")

        elif cmd[0] == "set":
            if cmd[2] == "token":
                if cmd[1] == "user":
                    user_token = cmd[3]
                    config.set('Token', 'User', user_token)

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)

            elif cmd[1] == "tor":
                if cmd[2] == "host":
                    host = cmd[3]
                    config.set('Tor', 'host', host)

                elif cmd[2] == "port_range":
                    port_range = cmd[3]
                    config.set('Tor', 'port_range', port_range)
                    
                    port_range = config.get('Tor', 'port_range')
                    port1, port2 = port_range.split(',')
                    port1 = int(port1)
                    port2 = int(port2)
                    proxies = [f"{host}:{port}" for port in range(port1, port2)]

                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
            else:
                print("Usage: set <user/webhook> <token> / set <tor> <host/port_range>")
