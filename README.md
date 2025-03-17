# Jupyter MTH3026

A repository for working with JupyterLab and exporting notebooks to pdf.

If using for the first time, you'll need to create a Codespace for this repository. This is a
virtual computer than runs Jupyter and contains all the tools needed to convert to a PDF.

1. Visit this repository on GitHub (you've probably already done that).
2. Press the green 'Code' button.
3. Click on the Codespaces tab.
4. Click 'Create codespace on main' to create a new codespace

A browser window will open. It will take about 2 minutes to finish creating the Codespace. You'll
see a progress indicator 'Building codespace...' in the bottom right while this is happening. When
it's finished, you'll see an open Terminal pane in the bottom of the screen with a message something
like

```
(base) jovyan@codespaces-2151cd:/workspaces/jupytermth3026$
```

1. Click in the Terminal window and type either `jupyter notebook` or `jupyter lab` depending on
   whether you prefer the Notebook interface or the Jupyter Lab interface. If you have no
   preference, just type `jupyter notebook`.
2. You have now created a Jupyter server running on the remote machine that is forwarding a port to
   your local machine. Access the server by clicking on 'Ports' (where there will be a blue numbered
   circle). Click on the world icon 🌐 next to the URL of the forwarded addreess.
3. This opens up a Jupyter tab in your web browser. You should now upload your Jupyter notebook to
   the server via the upload button.
4. Double-click on the name of your notebook to open it. Check everything is correct and make
   changes if necessary.
5. From the File menu, select, 'Save and Export Notebook As...' then select 'PDF'.
6. Depending on your browser, you may need to 'allow downloads' and ensure pop-up windows aren't
   blocked.
7. The PDF will be downloaded to your local Downloads folder.

