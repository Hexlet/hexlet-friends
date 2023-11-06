## Main steps

1. Choose an issue in repo (`https://github.com/Hexlet/hexlet-friends/issues`)
2. Read comments and if nobody took it yet make a comment
3. Fork it
4. Clone repo ```git clone ssh://git@github.com/{your-nickname}/hexlet-friends.git```
5. Create your feature branch (`git checkout -b my-new-feature`)
6. Make changes
7. Checkout Makefile or README.md for commands like `make check` `make lint` `make test`
8. Run tests and linters (`make check`)
9. Commit your changes (`git commit -am 'Added some feature'`)
*When you install a project, scripts for pre-commit hooks are added to the .git folder.
When you make your first commit, you will see the environment setting for the hooks in the terminal.
This is normal behavior and will only happen on your first commit. In general, you will see in the terminal
the status of checks for pre-commit hooks. Some hooks will make edits automatically and clean files will be
added to the commit. Some (e.g. flake8) will display errors in the terminal and abort the commit to fix
them. In this case, fix the errors and try to commit again. You can read more about pre-commit hooks [here](https://pre-commit.com/).*
10. Push to the branch (`git push origin my-new-feature`)
11. Create new Pull Request
12. Check if Request passed GithubActions
13. Wait, until PR is reviewed
