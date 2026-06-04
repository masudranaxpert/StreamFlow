# Platforms

StreamFlow supports multiple video streaming platforms.

## Understanding the URLs

Most platforms expose **two distinct URLs**. They are not interchangeable —
mixing them up is the most common configuration mistake, so read this
once before scrolling down:

| Term | What it is | Used for | Parameter name |
|------|------------|----------|----------------|
| **API Base URL** | Host (and prefix) where the JSON API lives. Example: `https://voe.sx/api`. | Authenticated requests: upload, list files, account stats, delete, etc. | `base_url` |
| **Site URL** | Host that serves the **player / embed page / master link**. Example: `https://voe.sx`. The returned `streaming_url`, master URL and `/e/{filecode}` embed URL are all built from this host. | `get_master_link()`, building player/embed links. | `site_base_url` (or `base_url` on master-link-only helpers) |

> **TL;DR — Site URL = where the *video plays*. API Base URL = where the
> *API calls go*.** When a provider gives you a single domain like
> `seekstreaming.com`, that's the Site URL; the API is reachable at the
> same host with an `/api/v1` suffix.

## Available Platforms

| Platform | Default API Base URL | Description |
|----------|----------------------|-------------|
| [StreamEmbed](streamembed.md) | `https://seekstreaming.com/api/v1` | Master link + upload API (seekstreaming / streamp2p / player4me) |
| [VOE](voe.md) | `https://voe.sx/api` | Account stats, file management, master link (m3u8) |
| [Anonstream](anonstream.md) | `https://anonstream.co` (`/api/*` prefixed automatically) | Remote upload, file management |
| [Byse](byse.md) | `https://api.byse.sx` | Upload, file management, master link |
| [Vidara](vidara.md) | `https://api.vidara.so/v1` | Video upload, HLS streaming |

## StreamEmbed

StreamEmbed provides master link resolution (get m3u8 streaming URLs) and advance upload functionality for multiple providers.

**Providers** (all share the same `/api/v1` API surface, just on different hosts):

| Provider     | Site URL *(player / master link)* | API Base URL *(upload / management)*  |
|--------------|-----------------------------------|---------------------------------------|
| seekstreaming | `https://seekstreaming.com` | `https://seekstreaming.com/api/v1` |
| streamp2p     | `https://streamp2p.com`     | `https://streamp2p.com/api/v1`     |
| player4me     | `https://player4me.com`     | `https://player4me.com/api/v1`     |

> Use the **Site URL** when calling `get_master_link()` or building an
> embed URL via `embed_url(filecode)`. Use the **API Base URL** when
> instantiating `StreamembedClient` or calling `advance_upload()`.

**Features:**
- AES-128-CBC encrypted master link decryption
- Advance upload with progress tracking
- Proxy support (TCP, UDP, MASQUE)
- HTTP version selection (HTTP/1.1, HTTP/2, HTTP/3)

## VOE

VOE provides account management, file operations, and master link
resolution for voe.sx.

- **Provider:** voe.sx
- **API Base URL** *(JSON API: account, files, upload)*: `https://voe.sx/api`
- **Site URL** *(player / `/e/{filecode}` embed page / master link)*: `https://voe.sx`

**Features:**
- Account statistics
- File listing
- File deletion
- Purge all files
- Upload URL generation
- **Master link (m3u8) resolution** via `get_master_link()` — scrapes
  the player page at `/e/{filecode}` and decrypts the obfuscated
  source. No API key required.

## Anonstream

Anonstream provides remote upload and file management for anonstream.co.

- **Provider:** anonstream.co
- **Base URL:** `https://anonstream.co` *(the client prefixes `/api/` automatically; same host serves both site & API)*

**Features:**
- Remote URL upload (Google Drive supported)
- Account statistics
- File listing with filters
- File deletion
- Bulk purge

## Byse

Byse provides upload, file management, and master link resolution for byse.sx.

- **Provider:** byse.sx
- **API Base URL** *(JSON API: account, files, upload, master link)*: `https://api.byse.sx`
- **Site URL** *(player / embed)*: `https://byse.sx` *(only relevant if you build embed URLs yourself)*

**Features:**
- Remote upload
- Account statistics
- File listing
- File deletion
- Master link (m3u8 streaming URLs)
- Challenge auth support

## Vidara

Vidara provides video upload and HLS streaming for vidara.so.

- **Provider:** vidara.so
- **API Base URL** *(JSON API: upload, server)*: `https://api.vidara.so/v1`
- **Site URL** *(HLS streaming, `/api/stream`, `/e/{filecode}` embed)*: `https://vidara.so`

**Features:**
- Remote upload
- Upload server API
- Master link (HLS streaming)
- Proxy support
- HTTP version control