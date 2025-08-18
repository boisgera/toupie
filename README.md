Toupie
================================================================================

![Toupie](https://unsplash.com/photos/LiLPRqxWI9I/download?ixid=M3wxMjA3fDB8MXxzZWFyY2h8NHx8c3Bpbm5pbmclMjB0b3B8ZW58MHx8fHwxNzU1NTI1MTgzfDA&force=true&w=900)

Getting Started
--------------------------------------------------------------------------------

Get [uv] and start a toupie server with

```bash
uvx --from git+https://github.com/boisgera/toupie toupie
```

If you need additional Python dependencies, specify them with the `--with` flag.
For example:

```bash
uvx --with raylib --from git+https://github.com/boisgera/toupie toupie
```

> [!CAUTION]  
> Anyone that gets access to a running toupie server can do [a lot of damage]!

### Sanity check

To check that your toupie server works as expected, do

```bash
curl -X POST http://127.0.0.1:8000 -H "Content-Type: text/plain" --data-binary "print(1+1)"
```

or if `curl` is not available

```bash
uvx --with requests python -c "import requests; r = requests.post(url='http://127.0.0.1:8000', headers={'Content-Type': 'text/plain'}, data='print(1+1)'); print(r.text)"
```

In any case, you should see `2` printed in your terminal.

FAQ
--------------------------------------------------------------------------------

🚧 **TODO**

[uv]: https://docs.astral.sh/uv/
[a lot of damage]: https://www.youtube.com/watch?v=JZLAHGfznlY