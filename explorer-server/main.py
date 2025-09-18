import os
import logging
from datetime import datetime
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO)

mcp = FastMCP("File-Search")

ROOT_DIR = "/Users/jurepi/Downloads"

def search_files(keyword: str, base_path: str = ROOT_DIR, max_results: int = 20) -> list[dict]:
    results = []

    for dirpath, _, filenames in os.walk(base_path):
        for fname in filenames:

            if keyword.lower() in fname.lower():
                fpath = os.path.join(dirpath, fname)
                try:
                    stat = os.stat(fpath)

                    results.append({
                        "파일명": fname,
                        "경로": fpath,
                        "크기(Bytes)": stat.st_size,
                        "생성일": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M"),
                    })

                    if len(results) >= max_results:
                        return results
                except Exception as e:
                    logging.error(f"Error processing file {fname}: {e}")
                    continue
    return results

@mcp.tool()
def find_files(keyword: str) -> str:   
    """다운로드 디렉토리에서 파일명을 기준으로 키워드에 해당하는 파일을 검색합니다."""

    logging.info(f"'{keyword}' 키워드로 파일 검색 시작")
    found = search_files(keyword)

    if not found:
        return f"'{keyword}'에 해당하는 파일을 찾을 수 없습니다."

    response = "\n".join([f"{f['파일명']} - ({f['크기(Bytes)']} Bytes) - {f['경로']}" for f in found])
    return response

if __name__ == "__main__":
    mcp.run(transport="stdio")
