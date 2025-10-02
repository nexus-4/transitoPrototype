import os
import subprocess

def run_colmap_pipeline(image_dir: str, workspace_dir: str):
    """"
    Executa o pipiline do COLMAP para reconstrucao 3D.

    Args:
        image_dir (str): Diretorio contendo as imagens de entrada.
        workspace (str): Diretorio onde os resultados serao salvos.
    
    Returns:
        str: Caminho para a pasta de reconstrucao densa.
"""
    print("Iniciando o pipeline do COLMAP...")

    # Definicao dos caminhos
    db_path    = os.path.join(workspace_dir, "database.db")
    sparse_dir = os.path.join(workspace_dir, "sparse")
    dense_dir  = os.path.join(workspace_dir, "dense")

    # Garante que os diretorios de saida existam
    os.makedirs(sparse_dir, exist_ok=True)
    os.makedirs(dense_dir, exist_ok=True)

    # Execucao dos comandos do COLMAP
    # O argumento 'check=True' faz com que o script pare se algum comando falhar

    print("1. Extraindo features das imagens...")
    subprocess.run([
        "colmap", "feature_extractor",
        "--database_path", db_path,
        "--image_path", image_dir
    ], check=True)

    print("2. Realizando o matching das features...")
    subprocess.run([
        "colmap", "exhaustive_matcher",
        "--database_path", db_path
    ], check=True)

    print("3. Reconstruindo a estrutura esparsa...")
    subprocess.run([
        "colmap", "mapper",
        "--database_path", db_path,
        "--image_path", image_dir,
        "--output_path", sparse_dir
    ], check=True)

    print("4. Reconstruindo a estrutura densa...")
    subprocess.run([
        "colmap", "image_undistorter",
        "--image_path", image_dir,
        "--input_path", os.path.join(sparse_dir, "0"),
        "--output_path", dense_dir,
        "--output_type", "COLMAP",
    ], check=True)

    print("5. Reconstrucao densa (patch_match_stereo)...")
    subprocess.run([
        "colmap", "patch_match_stereo",
        "--workspace_path", dense_dir
    ], check=True)

    print("Pipeline do COLMAP concluido com sucesso!")

    return dense_dir
