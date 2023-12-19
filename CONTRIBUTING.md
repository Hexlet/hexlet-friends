## Main steps

1. Choose an issue in repo (`https://github.com/Hexlet/hexlet-friends/issues`)
2. Read comments and if nobody took it yet make a comment
3. Fork it
4. Clone repo ```git clone ssh://git@github.com/{your-nickname}/hexlet-friends.git```
5. Create your feature branch (`git checkout -b my-new-feature`)
6. Make changes
7. Checkout Makefile or README.md for commands like `make check` `make lint` `make test`
8. Run tests and linters (`make check`)
9. If your changes required database migrations, you should also update the erd-diagrams with the commands:  
```make erd-in-png```  
```make erd-in-pdf```
10. Commit your changes (`git commit -am 'Added some feature'`)
    * "When you install a project, scripts for the flake8 pre-commit hooks are added to the .git folder.  
    When you make your first commit, you will see the environment settings for the pre-commit hook displayed
    in the terminal. This is normal behavior and will only happen  
    on your first commit. In general, you will see in the terminal the status of the flake8 check for the pre-commit hook. 
    In case of linter errors, they will be displayed in the  
    terminal and abort the commit to fix them. If there are any errors, fix these errors and try to commit again. You can read more about pre-commit hooks [here](https://pre-commit.com/).*
11. Push to the branch (`git push origin my-new-feature`)
12. Create new Pull Request
13. Check if Request passed GithubActions
14. Wait, until PR is reviewed
