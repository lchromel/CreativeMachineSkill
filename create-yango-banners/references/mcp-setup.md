# Install and verify Creative Machine MCP

## Connection contract

Install/update `create-yango-banners` and configure the MCP connection separately. SkillStore distributes instructions and references, not an authenticated connection. The Codex plugin also declares a server, but the user must supply its credential.

| Setting | Value |
| --- | --- |
| Server name | `yango-creative-machine` |
| Transport | Streamable HTTP |
| MCP URL | `https://creativemachiemcp-production.up.railway.app/mcp` |
| Authentication | `Authorization: Bearer <token>` |
| Local credential name | `CREATIVE_MACHINE_API_TOKEN` (raw token, without `Bearer `) |
| Public health check | `https://creativemachiemcp-production.up.railway.app/health` |

The website root is not the MCP endpoint; `/health` proves only that the process is alive. The MCP token must match the deployed server's `MCP_API_TOKEN`. It is separate from generator Basic Auth, provider keys, video passwords, and SkillStore authentication. Never put it in a URL, a shared skill, a repository, or an agent reply.

Use the user's designated credential file first if one was provided. A token saved in a text file does not automatically become an environment variable. Read only the named credential; do not source an arbitrary token document as a shell script. If missing or invalid, ask for the correct credential without displaying its value.

## Guided setup with a personal token file

For a client that supports Bearer authentication, help the user finish setup rather than only showing configuration snippets:

1. Check the user's designated credential source first. Reuse an existing valid credential; do not ask the user to enter it again. If the target application only supports OAuth, explain that incompatibility before asking for a Bearer token.
2. If no credential is available and local file access exists, run `python3 scripts/prepare_token_file.py` from this skill's directory. It copies [the blank token template](../assets/creative-machine-token.env.example) to `~/.config/creative-machine/token.env` (Windows: `%USERPROFILE%/.config/creative-machine/token.env`) and returns JSON with its absolute `path`. It uses owner-only directory/file permissions (0700/0600) on POSIX and preserves existing files without reading their contents. Use `--path` only for an explicitly requested personal location. If Python is unavailable, create the same file using available file tools. Never overwrite an existing credential file or create a secret-bearing file inside a repository, installed skill, plugin, shared folder or publicly hosted artifact directory.
3. Return a clickable link to the actual personal file using the host's file-link format and absolute path. If the host cannot create a private local file, offer the blank template as a download with instructions to save a personal copy, or use the application's private credential UI. Do not pretend to have created a file in an inaccessible environment, and never upload a filled credential file for linking.
4. Explain exactly what to fill, in the user's language. For example: «Создал [файл для токена](ABSOLUTE_PERSONAL_FILE_PATH). Вставь токен после `CREATIVE_MACHINE_API_TOKEN=`, сохрани файл и напиши “готово”. Сам токен в чат присылать не нужно». Replace the link placeholder with the real path. Pause authentication-dependent work until the file has been filled; do not generate a replacement image while waiting.
5. After the user confirms, read only `CREATIVE_MACHINE_API_TOKEN` from that file as data. Reject an empty value/placeholder; never execute/source the document. Do not print the value, include it in tool arguments or shell history, or expose it through config-dump output.
6. Configure the actual client with that credential using its supported private secret/header settings, preserving unrelated configuration. On a local Codex host that cannot inherit an environment variable, a private `http_headers.Authorization` entry is supported; create/retain owner-only permissions on the private config. Do not write both a stale bearer env reference and a new conflicting header. For another application, use its documented secret mechanism. If its settings are not accessible to the agent, guide the user to enter the credential there; report the remaining manual step honestly.
7. Restart/reconnect the MCP server, then perform the acceptance check from the application. Report setup complete only after actual MCP calls succeed. A filled file, a saved config or a successful external HTTP probe alone is insufficient. Do not delete the user's credential file after configuring the client unless asked.

This template contains no token and is safe to distribute. Only its personal copy should be filled. Reading a private credential for authorized MCP setup is setup work; it does not permit direct HTTP media generation outside MCP.

If an old client configuration reports missing `MCP_API_TOKEN`, inspect the credential setting for this connection. New client templates use `CREATIVE_MACHINE_API_TOKEN`; the server's Railway variable remains `MCP_API_TOKEN`. Align the client with the named credential source or a supported private header; do not rename the deployed server variable. A missing client environment variable is a setup task, not evidence that the user must edit the server.

## Codex desktop, CLI and IDE

Configure the same Codex host that will run the task. Merge this block into its private `~/.codex/config.toml`; preserve other servers and existing settings:

```toml
[mcp_servers.yango-creative-machine]
url = "https://creativemachiemcp-production.up.railway.app/mcp"
bearer_token_env_var = "CREATIVE_MACHINE_API_TOKEN"
startup_timeout_sec = 30
tool_timeout_sec = 1500
```

Alternatively, register the connection with the CLI, then set the timeouts in the config:

```sh
codex mcp add yango-creative-machine --url https://creativemachiemcp-production.up.railway.app/mcp --bearer-token-env-var CREATIVE_MACHINE_API_TOKEN
```

Make the raw token available in the environment of the actual Codex process. Exporting it in one terminal does not configure an already-running desktop app. For a GUI that cannot inherit the variable, use its private HTTP-header setting / `http_headers` with `Authorization: Bearer <token>`, keeping the value out of shared files. Choose one credential method; remove a stale conflicting Authorization value when changing methods.

The bundled Codex plugin already contains the production URL and the bearer environment-variable name. Supply the variable and enable the plugin's server; do not add a second duplicate connection unless replacing the plugin-provided one. Restart the connection/application, open a fresh task, and verify the actual tools below. A plugin dependency URL alone does not supply a token.

See [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp?surface=cli).

### Terminal entry and stale credentials

Use the personal-file workflow by default. If the user is already using terminal entry, diagnose that path instead of assuming they edited a file. Ask for the complete command without the token if it is cropped or unavailable.

First inspect this connection's configured credential name without printing credentials. The current plugin uses `CREATIVE_MACHINE_API_TOKEN`. Align a legacy client setting that still points to `MCP_API_TOKEN` with the current client name before prescribing a command. Leave the server's Railway `MCP_API_TOKEN` setting unchanged. Do not change unrelated MCP connections.

For terminal entry on macOS with the current environment-based client configuration, provide this complete command in a fenced code block, exactly with literal underscores:

```sh
python3 -c 'import getpass,subprocess; subprocess.run(["launchctl","setenv","CREATIVE_MACHINE_API_TOKEN",getpass.getpass("Token: ")],check=True)'
```

Explain that the user types the raw token into the hidden prompt, then fully quits Codex with Command-Q and reopens it. This command updates the user launch environment; it does not change the client configuration or update the environment of an already-running process. Do not use it for a client configured with private headers or OAuth. If a credential is already saved in the selected personal file, configure from that file instead of asking for another terminal entry.

When troubleshooting the reported token:

- `getpass` reads the submitted line; this command contains no truncation or nine-character limit. An environment read by the still-running agent may return an old value. Do not describe that value as the token the user just typed.
- In executable code, `MCP\_API\_TOKEN` contains literal backslashes and names a different variable from `MCP_API_TOKEN`. Never escape underscores inside fenced shell/Python commands. If backslashes appear only in a pasted Markdown representation, establish whether they were actually in the executed command before assigning the cause.
- Track the sources separately: the user's selected file, the variable saved through `launchctl`, the current process environment, and the client's configured credential source. Inspect only the named credential; capture sensitive command output internally and report source names and match/mismatch or presence, not values. Never run a bare `launchctl getenv` or dump a client config into visible tool output.
- A reported length such as nine characters is meaningful only for the specific source freshly inspected. Do not infer the user's token length from a placeholder, a cached process environment, or another variable. No fixed token length is specified by this service. Treat a 401/403 as observed only after an actual response, not as a prediction based on length.
- After a name/source correction and restart, check the actual MCP connection and call `get_banner_capabilities`. If tools are still absent, report that the client has not loaded/reconnected; do not blame the freshly entered token without evidence. If the intended source cannot be inspected from this task, state that limit and give the precise next verification step.

## Claude Code

Merge the following into the project's `.mcp.json`, preserving existing server entries. Claude Code expands the environment reference in `headers`; the Codex plugin's bearer field is not a substitute for this configuration.

```json
{
  "mcpServers": {
    "yango-creative-machine": {
      "type": "http",
      "url": "https://creativemachiemcp-production.up.railway.app/mcp",
      "headers": {
        "Authorization": "Bearer ${CREATIVE_MACHINE_API_TOKEN}"
      },
      "timeout": 1500000
    }
  }
}
```

Supply the raw token to the Claude Code process, approve this project connection when prompted, restart/reconnect, and check `/mcp`. A saved entry or unresolved `${CREATIVE_MACHINE_API_TOKEN}` is not a successful connection. See [Claude Code MCP setup](https://code.claude.com/docs/en/mcp).

## Claude Desktop, ChatGPT web and other clients

Check the actual application's supported transports and authentication before editing its settings. Use the connection contract above in a client that accepts Streamable HTTP and a Bearer token/custom Authorization header. Placeholder expansion and config filenames differ by application; never assume Claude Code's `.mcp.json` is portable to every client. A stdio-only client requires a separately installed, trusted MCP transport bridge supporting authenticated Streamable HTTP; a remote URL is not a stdio command.

The current deployment implements static Bearer authentication and does not implement an OAuth authorization server or discovery. A connector that only offers OAuth or unauthenticated access cannot authenticate to this deployment as-is. ChatGPT web's documented developer-mode choices are OAuth, No Authentication and Mixed Authentication; local Codex configuration is not imported there. Supporting such a connector requires the server operator to deploy a compatible OAuth integration and then register/connect it in that application. Do not describe this step as completed, select No Authentication for this protected server, disable server authentication, or put the shared token in the URL as a workaround.

See [ChatGPT developer-mode authentication](https://developers.openai.com/api/docs/guides/developer-mode). Confirm the target client's current official documentation if its connection UI differs. Until a compatible authenticated MCP connection exists, stop creative work and report the setup gap.

## Acceptance check in the actual application

1. Discover the connected server and its tools. At this release it exposes 56 tools; check required names and capabilities rather than hard-coding that count for future versions.
2. Call this server's `get_banner_capabilities`. Confirm expected services, brands and placements.
3. Call `get_upstream_readiness` and inspect readiness; call `get_source_catalog` with `catalog: "vehicles"` to verify access to the generator. These checks do not generate paid media.
4. Report the real tool names and the results. Only a successful call from the colleague's application proves that their application is connected; a separate terminal HTTP probe does not.
5. After a server/skill update, refresh the server tools and update the installed SkillStore copy, then start a fresh task. Previously installed copies are not replaced by a server deploy.

Full example request for the colleague:

> Используй create-yango-banners. Сначала проверь подключение к Yango Creative Machine MCP: вызови get_banner_capabilities, get_upstream_readiness и get_source_catalog для vehicles. Сообщи, какие вызовы действительно прошли и доступен ли генератор. Пока ничего не генерируй. Если MCP не подключён или авторизация не работает, остановись и укажи, что нужно исправить в подключении.

## Diagnose failures

| Symptom | Next action |
| --- | --- |
| Skill appears, MCP tools absent | Configure/enable the server in this application and refresh its tool catalogue. |
| 401/403 from `/mcp` | Check the MCP credential, the process environment and competing auth settings; do not replace it with an upstream/provider token. |
| Capabilities succeed but readiness/catalogue fail | Server connection works; inspect upstream credentials/service health on the server. |
| OAuth login/discovery fails | This deployment is Bearer-only; use a compatible client or have the operator add OAuth. |
| Tool call times out | Prefer advanced queued operations and poll existing IDs; never resubmit an unknown paid operation just because the client timed out. |
| Finished banner has no renderer call | Review the tool-call history and returned URLs. Source generation, uploads and saved settings alone do not prove a finished banner was rendered. |

The MCP-only rule is an agent instruction, not a technical sandbox over the host's other tools. For an enforced restriction, the host/operator must also restrict competing media tools for this workflow. Never promise universal enforcement solely from installing the skill.
