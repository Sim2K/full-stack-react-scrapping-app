import React, { useState } from 'react';
import { Box, Button, TextField, Paper, Typography } from '@mui/material';

const ScrapeForm = ({ onSubmit, isLoading }) => {
  const [url, setUrl] = useState('');
  const [instruction, setInstruction] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ url, instruction });
  };

  return (
    <Paper elevation={3} sx={{ p: 3, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Web Scraping with LLM
      </Typography>
      <form onSubmit={handleSubmit}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <TextField
            label="URL"
            variant="outlined"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            required
            fullWidth
            placeholder="https://example.com"
          />
          <TextField
            label="Instruction for LLM"
            variant="outlined"
            value={instruction}
            onChange={(e) => setInstruction(e.target.value)}
            multiline
            rows={4}
            fullWidth
            placeholder="Enter instructions for the LLM (e.g., 'Extract main topics and key points from this page')"
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={isLoading}
            sx={{ mt: 2 }}
          >
            {isLoading ? 'Processing...' : 'Extract Content'}
          </Button>
        </Box>
      </form>
    </Paper>
  );
};

export default ScrapeForm;
