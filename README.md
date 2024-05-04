<img width="100px" src="./images/depotify.png" />

# Depotify

[Github](https://github.com/philipstuessel/depotify)

```bash
jap i depotify
```

Depotify optimizes access to software packages by working specifically with the releases of GitHub projects. This package manager uses the GitHub API to specifically access the published releases within the GitHub repositories. Users can thus directly download the stable versions of software and their dependencies, which increases the reliability and security of the development environments. By focusing on releases, Depotify avoids common problems that can be associated with accessing running or unfinished code versions. This approach makes Depotify particularly suitable for developers who value stable and tested software versions.

---

### require package
```sh
depotify require <owner/repo>
```
or with version example: `<owner/repo>:1.2.4`

### uninstall package
```sh
depotify uninstall <owner/repo>
```

### initialize depotify.json
```sh
depotify init
```
### from depotify.json packages install
```sh
depotify install
```
### update all packages
```sh
depotify update
```

### list all: require
```sh
depotify list
```
---

## Function commands

### show depotify version
```sh
depotify v
```

### add the GitHub token
```sh
depotify gh token <token>
```

### show your token
```sh
depotify gh token
```

### clear cache
```sh
depotify clear:cache
```