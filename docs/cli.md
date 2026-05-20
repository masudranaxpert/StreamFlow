# CLI Usage

StreamFlow provides a command-line interface for quick access to platform operations.

## Usage

```bash
python -m streamflow <command>
```

## Commands

### Show All Platforms

```bash
python -m streamflow all
```

Shows help for all available platforms.

### Show Specific Platform

```bash
python -m streamflow <platform>
```

Available platforms:
- `streamembed` - StreamEmbed platform
- `voe` - VOE platform

### StreamEmbed

```bash
# Show all providers
python -m streamflow streamembed

# Show specific provider
python -m streamflow streamembed seekstreaming
python -m streamflow streamembed streamp2p
python -m streamflow streamembed player4me
```

### VOE

```bash
# Show VOE platform help
python -m streamflow voe
```

## Help Output

Each platform shows:
- Supported providers
- API endpoints
- Usage examples
- Parameter descriptions

## Examples

### Get Help

```bash
# All platforms
python -m streamflow all

# StreamEmbed with provider
python -m streamflow streamembed seekstreaming

# VOE
python -m streamflow voe
```

### From Python

```python
from streamflow.platforms.streamembed.help import show_help
from streamflow.platforms.voe.help import show_help as voe_help

# StreamEmbed help
show_help(provider="seekstreaming")

# VOE help
voe_help()
```

## Return Codes

| Code | Description |
|------|-------------|
| 0 | Success |
| 1 | Error (unknown platform, invalid provider, etc.) |