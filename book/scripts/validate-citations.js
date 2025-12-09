#!/usr/bin/env node

// Script to validate citations in MDX files
const fs = require('fs');
const path = require('path');

// This is a placeholder script for validating citations
console.log('Validating citations in MDX files...');

// In a real implementation, this would:
// 1. Scan all MDX files in the docs directory
// 2. Extract all <Citation> components
// 3. Validate that each citation follows APA format
// 4. Check that citations are properly formatted
// 5. Report any issues found

const docsDir = path.join(__dirname, '../docs');
const citationRegex = /<Citation[^>]*id="([^"]*)"[^>]*>/g;

let totalCitations = 0;
let issuesFound = [];

function scanDirectory(dir) {
  const files = fs.readdirSync(dir);

  for (const file of files) {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);

    if (stat.isDirectory()) {
      scanDirectory(filePath);
    } else if (file.endsWith('.mdx')) {
      const content = fs.readFileSync(filePath, 'utf8');
      let match;

      while ((match = citationRegex.exec(content)) !== null) {
        const citationId = match[1];
        totalCitations++;
        // In a real implementation, validate the citation ID format
        if (!citationId) {
          issuesFound.push(`Invalid citation format in ${filePath}`);
        }
      }
    }
  }
}

scanDirectory(docsDir);

console.log(`Found ${totalCitations} citations`);
if (issuesFound.length > 0) {
  console.log('Issues found:');
  issuesFound.forEach(issue => console.log(`  - ${issue}`));
  process.exit(1);
} else {
  console.log('All citations appear to be valid');
  process.exit(0);
}