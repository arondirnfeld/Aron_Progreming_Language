// rtl-utils.js
// Utility functions for RTL formatting in VS Code extension

/**
 * Format Aron code for better RTL display
 * @param {string} code - The Aron code to format
 * @returns {string} - The formatted code
 */
function formatAronCode(code) {
    const lines = code.split('\n');
    const formattedLines = [];
    let indentLevel = 0;
    
    // Keywords that increase indent
    const indentKeywords = ['אם'];
    // Keywords that decrease indent
    const dedentKeywords = ['סוף', 'אחרת'];
    
    for (const line of lines) {
        const stripped = line.trim();
        
        // Check for dedent keywords before processing this line
        if (dedentKeywords.some(keyword => stripped.startsWith(keyword))) {
            indentLevel = (indentLevel > 0) ? indentLevel - 1 : 0;
        }
        
        // Format the line with proper RTL-friendly indentation
        if (stripped && !stripped.startsWith('#')) {
            // Calculate right-side padding for RTL display
            const padding = '\u00A0'.repeat(4 * indentLevel);  // non-breaking space
            const formattedLine = padding + stripped;
            formattedLines.push(formattedLine);
        } else {
            formattedLines.push(line); // Keep comments and empty lines as is
        }
        
        // Check for indent keywords after processing this line
        if (indentKeywords.some(keyword => stripped.startsWith(keyword))) {
            indentLevel += 1;
        }
    }
    
    return formattedLines.join('\n');
}

/**
 * Add RTL marks to improve display of Hebrew text
 * @param {string} code - The code to add RTL marks to
 * @returns {string} - The code with RTL marks
 */
function addRtlMarks(code) {
    // Add RTL mark at the beginning of each Hebrew text section
    const rtlMark = '\u200F';  // Right-to-Left Mark
    
    const containsHebrew = (text) => /[א-ת]/.test(text);
    
    const lines = code.split('\n');
    const rtlLines = lines.map(line => {
        // Don't add RTL marks to empty lines or comments
        if (!line.trim() || line.trim().startsWith('#')) {
            return line;
        }
        
        // Add RTL mark if line contains Hebrew characters
        if (containsHebrew(line)) {
            return rtlMark + line;
        }
        return line;
    });
    
    return rtlLines.join('\n');
}

module.exports = {
    formatAronCode,
    addRtlMarks
};
