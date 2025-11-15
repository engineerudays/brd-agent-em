// Prepare filename and data for file writing - BOTH JSON AND TXT
// Copy this entire code into the "Prepare File Data" node in n8n

const planData = $input.item.json;
const brdName = planData._filename_data?.brd_name || 'unknown_project';
const timestamp = planData._filename_data?.timestamp || new Date().toISOString().replace(/:/g, '-').split('.')[0];

// Sanitize BRD name for filename
const sanitizedName = brdName
  .toLowerCase()
  .replace(/\s+/g, '_')
  .replace(/[^a-z0-9_-]/g, '')
  .substring(0, 50);

// Remove internal fields from output
const cleanData = { ...planData };
delete cleanData._filename_data;

// Create filenames
const filenameJson = `engineering_plan_${sanitizedName}_v1_${timestamp}.json`;
const filenameTxt = `engineering_plan_${sanitizedName}_v1_${timestamp}.txt`;

// File paths
const filepathJson = `/data/projects/IK/brd_agent_em/sample_inputs/outputs/engineering_plans/${filenameJson}`;
const filepathTxt = `/data/projects/IK/brd_agent_em/sample_inputs/outputs/engineering_plans/${filenameTxt}`;

// ========== CREATE HUMAN-READABLE TEXT VERSION ==========
const plan = cleanData.engineering_plan || {};
const metadata = cleanData.metadata || {};

let txt = `╔═══════════════════════════════════════════════════════════════════════╗
║                        ENGINEERING PLAN                               ║
║                ${(metadata.source_brd || 'Project').substring(0, 50).padEnd(50)}                ║
╚═══════════════════════════════════════════════════════════════════════╝

Generated: ${metadata.timestamp || 'N/A'}
AI Model: ${metadata.ai_model || 'N/A'}
Tokens Used: ${metadata.tokens_used?.input || 0} input, ${metadata.tokens_used?.output || 0} output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 PROJECT OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Name: ${plan.project_overview?.name || 'N/A'}

📝 Description:
${plan.project_overview?.description || 'N/A'}

🎯 Objectives:
${(plan.project_overview?.objectives || []).map((obj, i) => `  ${i + 1}. ${obj}`).join('\n')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 FEATURE BREAKDOWN (${(plan.feature_breakdown || []).length} features)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;

(plan.feature_breakdown || []).forEach((feature, idx) => {
  txt += `\n[${idx + 1}] ${feature.feature_name || 'Unnamed Feature'} (${feature.feature_id || 'N/A'})\n`;
  txt += `    Priority: ${feature.priority || 'N/A'} | Complexity: ${feature.complexity || 'N/A'} | Effort: ${feature.estimated_effort || 'N/A'}\n`;
  txt += `    Description: ${feature.description || 'N/A'}\n`;
  if (feature.dependencies && feature.dependencies.length > 0) {
    txt += `    Dependencies: ${feature.dependencies.join(', ')}\n`;
  }
  if (feature.technical_requirements && feature.technical_requirements.length > 0) {
    txt += `    Technical Requirements:\n`;
    feature.technical_requirements.forEach(req => {
      txt += `      • ${req}\n`;
    });
  }
  if (feature.acceptance_criteria && feature.acceptance_criteria.length > 0) {
    txt += `    ✓ Acceptance Criteria:\n`;
    feature.acceptance_criteria.forEach(criteria => {
      txt += `      • ${criteria}\n`;
    });
  }
});

txt += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏗️  TECHNICAL ARCHITECTURE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;

const arch = plan.technical_architecture || {};
if (arch.system_components && arch.system_components.length > 0) {
  txt += `📦 System Components:\n${arch.system_components.map(c => `  • ${c}`).join('\n')}\n\n`;
}
if (arch.integration_points && arch.integration_points.length > 0) {
  txt += `🔌 Integration Points:\n${arch.integration_points.map(i => `  • ${i}`).join('\n')}\n\n`;
}
if (arch.data_flow) {
  txt += `🔄 Data Flow:\n  ${arch.data_flow}\n\n`;
}
if (arch.security_considerations && arch.security_considerations.length > 0) {
  txt += `🔒 Security Considerations:\n${arch.security_considerations.map(s => `  • ${s}`).join('\n')}\n`;
}

txt += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 IMPLEMENTATION PHASES (${(plan.implementation_phases || []).length} phases)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;

(plan.implementation_phases || []).forEach((phase, idx) => {
  txt += `\nPhase ${phase.phase_number || idx + 1}: ${phase.phase_name || 'Unnamed Phase'}\n`;
  txt += `Duration: ${phase.estimated_duration || 'N/A'}\n`;
  txt += `Description: ${phase.description || 'N/A'}\n`;
  if (phase.features_included && phase.features_included.length > 0) {
    txt += `Features: ${phase.features_included.join(', ')}\n`;
  }
  if (phase.deliverables && phase.deliverables.length > 0) {
    txt += `Deliverables:\n${phase.deliverables.map(d => `  ✓ ${d}`).join('\n')}\n`;
  }
});

txt += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  RISK ANALYSIS (${(plan.risk_analysis || []).length} risks identified)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;

(plan.risk_analysis || []).forEach((risk, idx) => {
  txt += `\n[${risk.risk_id || `R${idx + 1}`}] Impact: ${risk.impact || 'N/A'} | Probability: ${risk.probability || 'N/A'}\n`;
  txt += `Description: ${risk.description || 'N/A'}\n`;
  txt += `Mitigation: ${risk.mitigation_strategy || 'N/A'}\n`;
});

txt += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 RESOURCE REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;

const resources = plan.resource_requirements || {};
if (resources.team_composition && resources.team_composition.length > 0) {
  txt += `Team Composition:\n${resources.team_composition.map(t => `  • ${t}`).join('\n')}\n\n`;
}
if (resources.tools_and_technologies && resources.tools_and_technologies.length > 0) {
  txt += `Tools & Technologies:\n${resources.tools_and_technologies.map(t => `  • ${t}`).join('\n')}\n\n`;
}
if (resources.infrastructure_needs && resources.infrastructure_needs.length > 0) {
  txt += `Infrastructure Needs:\n${resources.infrastructure_needs.map(i => `  • ${i}`).join('\n')}\n`;
}

txt += `\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 SUCCESS METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

`;

(plan.success_metrics || []).forEach((metric, idx) => {
  txt += `${idx + 1}. ${metric.metric_name || 'Unnamed Metric'}\n`;
  txt += `   Target: ${metric.target_value || 'N/A'}\n`;
  txt += `   Measurement: ${metric.measurement_method || 'N/A'}\n\n`;
});

txt += `\n╔═══════════════════════════════════════════════════════════════════════╗
║                           END OF REPORT                               ║
╚═══════════════════════════════════════════════════════════════════════╝\n`;

// ========== CREATE BINARY DATA FOR BOTH FILES ==========

// JSON file
const jsonString = JSON.stringify(cleanData, null, 2);
const jsonBinary = Buffer.from(jsonString, 'utf-8');

// TXT file
const txtBinary = Buffer.from(txt, 'utf-8');

// Return BOTH files (n8n will process each item separately)
return [
  {
    json: {
      filename: filenameJson,
      filepath: filepathJson,
      format: 'json'
    },
    binary: {
      data: {
        data: jsonBinary.toString('base64'),
        mimeType: 'application/json',
        fileName: filenameJson
      }
    }
  },
  {
    json: {
      filename: filenameTxt,
      filepath: filepathTxt,
      format: 'txt'
    },
    binary: {
      data: {
        data: txtBinary.toString('base64'),
        mimeType: 'text/plain',
        fileName: filenameTxt
      }
    }
  }
];

