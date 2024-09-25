import streamlit as st
import pubchempy as pcp
import rdkit.Chem as Chem
from rdkit.Chem import AllChem
import py3Dmol

# Streamlit app title
st.title("Chemical Information and 3D Viewer")

# Step 1: Create a text input box in Streamlit for the chemical name
chemical_name = st.text_input("Enter chemical name:")

if chemical_name:
    try:
        # Fetch the compound from PubChem by name
        compound = pcp.get_compounds(chemical_name, 'name')[0]

        # Step 2: Display chemical information
        st.write(f"**IUPAC Name:** {compound.iupac_name}")
        st.write(f"**Common Name:** {compound.synonyms[0]}")
        st.write(f"**Molecular Weight:** {compound.molecular_weight}")
        st.write(f"**Formula:** {compound.molecular_formula}")
        
        # Step 3: Display SMILES notation
        smiles = compound.canonical_smiles
        st.write(f"**SMILES:** {smiles}")

        # Step 4: Generate 3D coordinates of the molecule
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)  # Add hydrogen atoms
        AllChem.EmbedMolecule(mol, AllChem.ETKDG())  # Generate 3D coordinates
        mol_block = Chem.MolToMolBlock(mol)

        # Step 5: Create a py3Dmol viewer
        viewer = py3Dmol.view(width=400, height=400)
        viewer.addModel(mol_block, "mol")  # Add molecule to the viewer
        viewer.setStyle({'stick': {'colorscheme': 'Jmol'}})  # Set color scheme
        viewer.zoomTo()

        # Step 6: Render the py3Dmol viewer in Streamlit
        viewer.render()  # Ensure compatibility with Streamlit
        viewer_html = viewer._make_html()  # Get the HTML for Streamlit
        st.components.v1.html(viewer_html, height=400)

        # Step 7: Display the color legend for the atoms
        st.markdown("""
        **Legend:**
        - Carbon (C) - Light Gray
        - Oxygen (O) - Red
        - Nitrogen (N) - Blue
        - Hydrogen (H) - White
        - Sulfur (S) - Yellow
        - Phosphorus (P) - Orange
        """)

    except IndexError:
        st.error(f"No information found for {chemical_name}.")
