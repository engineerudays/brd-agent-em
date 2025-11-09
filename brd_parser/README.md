# BRD Parser Module

This module handles the parsing and processing of Business Requirements Documents (BRDs).

## Structure

- `workflows/` - Additional workflow files for BRD parsing
- `schemas/` - JSON schemas for validating BRD structure
- `utils/` - Helper scripts and utilities for BRD processing

## Main Workflow File

⚠️ **Important Submission Requirement:**

The primary BRD parser workflow should be placed directly in this directory:
- **`brd_input_cleaner.json`** - Exported from n8n BRD Input Parser flow (place at `brd_parser/brd_input_cleaner.json`)

For MVP development, you may organize files in subdirectories, but ensure the final submission follows the required structure with `brd_input_cleaner.json` at the root of the `brd_parser/` folder.

## Purpose

- Parse incoming BRD documents
- Clean and validate BRD input
- Extract key information from BRDs
- Transform BRDs into structured data
- Route to appropriate agents (Planning or Design)

## Integration with Multi-Agent System

The BRD Parser is the entry point for the entire system:
1. Receives raw BRD input
2. Cleans and validates the document
3. Extracts structured information
4. Routes to Planning Agent or Design Agent based on requirements

