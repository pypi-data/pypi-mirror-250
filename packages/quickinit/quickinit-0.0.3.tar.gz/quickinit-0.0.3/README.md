# quickinit

quickinit is a command line tool to quickly generate project structures for different programming languages and frameworks. 

## Features

- Generate project structure for:
    - Python 
    - Golang
    - Vanilla Web (HTML, CSS, JS)
    - NextJS
    - Rust
- Open generated project in VSCode

## Usage

```
pip install quickinit
```

Run the script and answer the prompts:

1. Choose the programming language/framework stack 
2. Enter a project name

The tool will generate the basic project structure for you.

After generation, the project will be opened in VSCode automatically (if available on your system).

## Adding New Templates

To add additional templates:

1. Add a template folder under `templates/`
2. Update `create_[language]_project_structure()` to copy or generate the new template
3. Update the main prompt to include the new option
4. Update the main match statement to call the new project structure generation function

Or you can open an issue on the repo.

## To Do

- Add testing
- Improve error handling
- Add option to git init generated project
- Expand available templates

## License

This project is open source and available under the [MIT License](LICENSE).