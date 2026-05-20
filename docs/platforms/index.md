# Platforms

StreamFlow supports multiple video streaming platforms.

## Available Platforms

| Platform | Providers | Description |
|----------|-----------|-------------|
| [StreamEmbed](streamembed.md) | seekstreaming, streamp2p, player4me | Master link + upload API |
| [VOE](voe.md) | voe.sx | Account stats, file management |
| [Anonstream](anonstream.md) | anonstream.sx | Remote upload, file management |
| [Byse](byse.md) | byse.sx | Upload, file management, master link |
| [Vidara](vidara.md) | vidara.so | Video upload, HLS streaming |

## StreamEmbed

StreamEmbed provides master link resolution (get m3u8 streaming URLs) and advance upload functionality for multiple providers.

**Providers:**
- `seekstreaming` - https://seekstreaming.com
- `streamp2p` - https://streamp2p.com
- `player4me` - https://player4me.com

**Features:**
- AES-128-CBC encrypted master link decryption
- Advance upload with progress tracking
- Proxy support (TCP, UDP, MASQUE)
- HTTP version selection (HTTP/1.1, HTTP/2, HTTP/3)

## VOE

VOE provides account management and file operations for voe.sx.

**Provider:** voe.sx

**Features:**
- Account statistics
- File listing
- File deletion
- Purge all files
- Upload URL generation

## Anonstream

Anonstream provides remote upload and file management for anonstream.sx.

**Provider:** anonstream.sx

**Features:**
- Remote URL upload (Google Drive supported)
- Account statistics
- File listing with filters
- File deletion
- Bulk purge

## Byse

Byse provides upload, file management, and master link resolution for byse.sx.

**Provider:** byse.sx

**Features:**
- Remote upload
- Account statistics
- File listing
- File deletion
- Master link (m3u8 streaming URLs)
- Challenge auth support

## Vidara

Vidara provides video upload and HLS streaming for vidara.so.

**Provider:** vidara.so

**Features:**
- Remote upload
- Upload server API
- Master link (HLS streaming)
- Proxy support
- HTTP version control