// Extension for Aron Programming Language
const vscode = require('vscode');
const path = require('path');
const { exec } = require('child_process');

/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
    console.log('Aron Language Extension is now active!');

    // Register the command to run Aron files
    let runCommand = vscode.commands.registerCommand('aron.run', function() {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found!');
            return;
        }

        const document = editor.document;
        if (document.languageId !== 'aron') {
            vscode.window.showErrorMessage('This is not an Aron file!');
            return;
        }

        // Save the file before running it
        document.save().then(() => {
            const filePath = document.uri.fsPath;
            const terminal = vscode.window.createTerminal('Aron');
            terminal.show();

            // Find the main.py interpreter path
            // This assumes that the main.py is in the src directory which is a sibling to the vscode-aron-extension directory
            const extensionPath = context.extensionPath;
            const mainPyPath = path.join(path.dirname(extensionPath), 'src', 'main.py');
            
            // Run the Aron file
            terminal.sendText(`python "${mainPyPath}" "${filePath}"`);
        });
    });

    context.subscriptions.push(runCommand);

    // Register completion provider for Aron language
    const completionProvider = vscode.languages.registerCompletionItemProvider('aron', {
        provideCompletionItems(document, position, token, context) {
            // Create a list of completion items
            const completionItems = [];
            
            // Keywords
            const keywords = [
                { label: 'הדפס', detail: 'Print a value', documentation: 'Prints the value of an expression or a string.' },
                { label: 'קבע', detail: 'Declare variable', documentation: 'Declares a new variable or assigns a value to an existing one.' },
                { label: 'אם', detail: 'If statement', documentation: 'Begins a conditional block that executes if the condition is true.' },
                { label: 'אחרת', detail: 'Else statement', documentation: 'Specifies a block to execute when the if condition is false.' },
                { label: 'סוף', detail: 'End block', documentation: 'Marks the end of a control structure block like if-else.' },
                { label: 'אמת', detail: 'Boolean true', documentation: 'Boolean true value.' },
                { label: 'שקר', detail: 'Boolean false', documentation: 'Boolean false value.' }
            ];
            
            keywords.forEach(keyword => {
                const item = new vscode.CompletionItem(keyword.label, vscode.CompletionItemKind.Keyword);
                item.detail = keyword.detail;
                item.documentation = new vscode.MarkdownString(keyword.documentation);
                completionItems.push(item);
            });
            
            return completionItems;
        }
    });
    
    context.subscriptions.push(completionProvider);

    // Register hover provider for Aron language
    const hoverProvider = vscode.languages.registerHoverProvider('aron', {
        provideHover(document, position, token) {
            const wordRange = document.getWordRangeAtPosition(position);
            if (!wordRange) {
                return null;
            }
            
            const word = document.getText(wordRange);
            
            // Define hover content for keywords
            const hoverContent = {
                'הדפס': 'Print statement\n\nSyntax: `הדפס <expression>`\n\nPrints the value of the expression to the console.',
                'קבע': 'Variable declaration\n\nSyntax: `קבע <name> = <expression>`\n\nCreates a new variable or assigns a value to an existing one.',
                'אם': 'If statement\n\nSyntax: `אם <condition>\n    <statements>\nסוף`\n\nExecutes statements if the condition is true.',
                'אחרת': 'Else statement\n\nSyntax: `אם <condition>\n    <statements>\nאחרת\n    <statements>\nסוף`\n\nExecutes statements if the condition is false.',
                'סוף': 'End block\n\nMarks the end of a control structure block like if-else.',
                'אמת': 'Boolean true\n\nBoolean literal representing the true value.',
                'שקר': 'Boolean false\n\nBoolean literal representing the false value.'
            };
            
            if (hoverContent[word]) {
                return new vscode.Hover(new vscode.MarkdownString(hoverContent[word]));
            }
            
            return null;
        }
    });
    
    context.subscriptions.push(hoverProvider);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
