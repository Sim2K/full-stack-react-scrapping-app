import React from 'react';
import { Paper, Typography, Box, Tabs, Tab } from '@mui/material';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { materialDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const TabPanel = ({ children, value, index }) => (
  <div hidden={value !== index} style={{ padding: '20px 0' }}>
    {value === index && children}
  </div>
);

const ResultsView = ({ results }) => {
  const [tabValue, setTabValue] = React.useState(0);

  if (!results) return null;

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const renderJsonContent = (content) => {
    if (typeof content === 'string') {
      try {
        content = JSON.parse(content);
      } catch (e) {
        // If parsing fails, keep it as a string
      }
    }
    return (
      <SyntaxHighlighter language="json" style={materialDark}>
        {JSON.stringify(content, null, 2)}
      </SyntaxHighlighter>
    );
  };

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 4, maxWidth: '100%', overflow: 'auto' }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Results
      </Typography>

      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange}>
          <Tab label="Extracted Content" />
          <Tab label="Markdown" />
          <Tab label="Fit Markdown" />
          <Tab label="Raw Response" />
        </Tabs>
      </Box>

      <TabPanel value={tabValue} index={0}>
        {results.extracted_content ? (
          <Box sx={{ mt: 2 }}>
            {renderJsonContent(results.extracted_content)}
          </Box>
        ) : (
          <Typography color="textSecondary">No extracted content available</Typography>
        )}
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        <Box sx={{ mt: 2 }}>
          <ReactMarkdown>{results.markdown || ''}</ReactMarkdown>
        </Box>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        <Box sx={{ mt: 2 }}>
          <ReactMarkdown>{results.fit_markdown || ''}</ReactMarkdown>
        </Box>
      </TabPanel>

      <TabPanel value={tabValue} index={3}>
        <Box sx={{ mt: 2 }}>
          {renderJsonContent(results)}
        </Box>
      </TabPanel>
    </Paper>
  );
};

export default ResultsView;
