import streamlit as st
import pandas as pd
from browser_manager import BrowserManager
from element_scraper import ElementScraper
from snapshot_manager import SnapshotManager
from comparison_engine import ComparisonEngine
from config import DEFAULT_ELEMENTS

st.set_page_config(page_title="UI Change Monitor", layout="wide")
st.title("UI Change Monitor")
st.write("Track changes on your websites over time")

snapshot_manager = SnapshotManager()
comparison_engine = ComparisonEngine()

with st.sidebar:
    st.header("Controls")
    url = st.text_input("Website URL", "https://example.com")
    
    if st.button("Take Snapshot"):
        with st.spinner("Capturing page data..."):
            browser_manager = BrowserManager()
            if browser_manager.start_browser():
                try:                  
                    scraper = ElementScraper(browser_manager.driver)
                    page_info = scraper.scrape_page_info(url)

                    elements_data = {}
                    for name, selector in DEFAULT_ELEMENTS.items():
                        elements_data[name] = scraper.scrape_element(selector, name)

                    filename = snapshot_manager.save_snapshot(url, elements_data, page_info)
                    st.success(f"Snapshot saved: {filename}")
                    
                finally:
                    browser_manager.quit_browser()

st.header("Compare Snapshots")
snapshots = snapshot_manager.list_snapshots()

if len(snapshots) >= 2:
    col1, col2 = st.columns(2)
    with col1:
        snap_a = st.selectbox("First Snapshot", snapshots, index=1)
    with col2:
        snap_b = st.selectbox("Second Snapshot", snapshots, index=0)
    
    if st.button("Compare"):
        data_a = snapshot_manager.load_snapshot(snap_a)
        data_b = snapshot_manager.load_snapshot(snap_b)
        
        changes = comparison_engine.compare_snapshots(data_a, data_b)
        
        if changes:
            st.error(f"Found {len(changes)} changes!")
            df = pd.DataFrame(changes)
            st.dataframe(df)
        else:
            st.success("No changes detected!")

st.header("Recent Snapshots")
if snapshots:
    for snap in snapshots[:5]:
        data = snapshot_manager.load_snapshot(snap)
        st.write(f"**{snap}** - {data['metadata']['title']}")
else:
    st.info("No snapshots yet. Take your first snapshot using the sidebar!")