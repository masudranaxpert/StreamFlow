# Platforms

StreamFlow supports multiple video streaming platforms.

## Available Platforms

| Platform | Description |
|----------|-------------|
| [StreamEmbed](streamembed.md) | Master link resolution + upload API |
| [VOE](voe.md) | Account stats, file management |
| [Anonstream](anonstream.md) | Remote upload, file management |
| [Byse](byse.md) | Upload, file management, master link |
| [Vidara](vidara.md) | Video streaming platform |

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

VOE provides account management and file operations.

**Features:**
- Account statistics
- File listing
- File deletion
- Purge all files
- Upload URL generation