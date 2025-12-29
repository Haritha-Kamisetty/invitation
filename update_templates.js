// Convert JSON templates to JavaScript and update app.js
const fs = require('fs');

// Read the generated JSON
const templates = JSON.parse(fs.readFileSync('templates_output.json', 'utf8'));

// Convert to JavaScript format
let jsContent = 'const TEMPLATES = ' + JSON.stringify(templates, null, 4).replace(/"([^"]+)":/g, '$1:') + ';';

// Read current app.js
let appJs = fs.readFileSync('app/static/js/app.js', 'utf8');

// Find and replace the TEMPLATES object
const startMarker = 'const TEMPLATES = {';
const endMarker = '};';

const startIndex = appJs.indexOf(startMarker);
const endIndex = appJs.indexOf(endMarker, startIndex) + endMarker.length;

if (startIndex !== -1 && endIndex !== -1) {
    const before = appJs.substring(0, startIndex);
    const after = appJs.substring(endIndex);

    appJs = before + jsContent + after;

    fs.writeFileSync('app/static/js/app.js', appJs, 'utf8');
    console.log('✅ Successfully updated app.js with 90 templates!');
    console.log(`   - Birthday: ${templates.birthday.length} templates`);
    console.log(`   - Wedding: ${templates.wedding.length} templates`);
    console.log(`   - Anniversary: ${templates.anniversary.length} templates`);
    console.log(`   - Baby: ${templates.baby.length} templates`);
} else {
    console.error('❌ Could not find TEMPLATES object in app.js');
}
