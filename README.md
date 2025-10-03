# Reconstrução 3D com COLMAP

Ferramenta simples em **Streamlit** para gerar reconstrução 3D esparsa (nuvem de pontos inicial) a partir de um conjunto de fotos usando **COLMAP**.

Atualmente o pipeline implementado gera apenas o **modelo esparso** (estrutura inicial). Você pode opcionalmente ativar a reconstrução **densa**, gerar um PLY mais completo e converter para **Potree** para visualização web, caso seu ambiente suporte (CUDA/NVIDIA recomendado para performance).

---
## 📂 Estrutura do Projeto
```
app.py                  # Interface Streamlit
processing/pipeline.py  # Pipeline COLMAP (reconstrução esparsa; blocos para densa comentados)
requirements.txt        # Dependências Python (apenas Streamlit)
```

---
## ✅ Funcionalidades Atuais
- Upload de múltiplas imagens (JPG/PNG)
- Execução do pipeline COLMAP (feature extraction, matching, mapper)
- Conversão do modelo esparso para `sparse_model.ply`
- Download do resultado diretamente pela interface

---
## 🧩 Dependências
### Python
Instale via `pip`:
```
pip install -r requirements.txt
```
Somente `streamlit` é necessário no momento.

### Externas (não via pip)
| Ferramenta | Uso | Instalação (Exemplo) |
|------------|-----|----------------------|
| COLMAP | Reconstrução 3D | macOS: `brew install colmap`  / Ubuntu: `sudo apt install colmap` (ou build com CUDA) |
| CUDA (opcional) | Aceleração em GPU Nvidia | Instalar toolkit + driver (somente Linux/Windows) |
| PotreeConverter (opcional) | Converter nuvem de pontos para visualização web | Build a partir do repositório oficial |

> macOS (Apple Silicon) não suporta CUDA oficialmente; a execução será em CPU.

---
## 🚀 Execução
Após instalar o COLMAP e as dependências Python:
```
streamlit run app.py
```
Abra o link local exibido no terminal (geralmente `http://localhost:8501`).

---
## 🔧 Ativando Reconstrução Densa (Passo a Passo)
O arquivo `processing/pipeline.py` contém blocos comentados para a reconstrução densa. Para habilitar:

1. Procure pelas linhas comentadas envolvendo `dense_dir`, `image_undistorter` e `patch_match_stereo`.
2. Remova o bloco de string multi-linha que envolve essas chamadas. No código há um bloco iniciado próximo de:
   ```python
   ''''
       print("4. Desentortando as imagens para a reconstrucao densa...")
       subprocess.run([
           "colmap", "image_undistorter",
           "--image_path", image_dir,
           "--input_path", os.path.join(sparse_dir, "0"),
           # "--output_path", dense_dir,
           "--output_type", "COLMAP",
       ], check=True)

       print("5. Reconstrucao densa (patch_match_stereo)...")
       subprocess.run([
           "colmap", "patch_match_stereo",
           # "--workspace_path", dense_dir,
       ], check=True)
   '''
   ```
3. Substitua/edite para algo funcional como:
   ```python
   dense_dir = os.path.join(workspace_dir, "dense")
   os.makedirs(dense_dir, exist_ok=True)

   print("4. Desentortando as imagens para a reconstrucao densa...")
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
       "--workspace_path", dense_dir,
   ], check=True)

   print("6. Fusionando profundidades em nuvem de pontos densa...")
   dense_ply = os.path.join(workspace_dir, "dense_fused.ply")
   subprocess.run([
       "colmap", "stereo_fusion",
       "--workspace_path", dense_dir,
       "--input_type", "geometric",
       "--output_path", dense_ply,
   ], check=True)
   ```
4. Depois, você pode disponibilizar também `dense_fused.ply` para download da mesma forma que `sparse_model.ply`.

---
## 🌐 Conversão para Potree (Visualização Web)
Depois de gerar `dense_fused.ply` (ideal, mas pode ser usado o esparso):

1. Instale/compile o PotreeConverter (ex.: https://github.com/potree/PotreeConverter).
2. Execute:
   ```bash
   PotreeConverter /caminho/para/dense_fused.ply -o /caminho/para/potree_out --generate-page cena3d
   ```
3. Abra o arquivo `potree_out/cena3d.html` no navegador.

Se quiser automatizar, adicione no final do pipeline (exemplo simplificado):
```python
subprocess.run([
    "PotreeConverter", dense_ply,
    "-o", os.path.join(workspace_dir, "potree"),
    "--generate-page", "modelo_denso"
], check=True)
```
Certifique-se de que `PotreeConverter` esteja no PATH.

---
## ⚙️ CUDA (Opcional)
Para grande volume de imagens, CUDA acelera etapas de matching e reconstrução.

- Verifique se sua build do COLMAP tem suporte:
  ```bash
  colmap -h | grep CUDA || echo "Provavelmente sem suporte CUDA"
  ```
- Se não tiver, compile manualmente (Ubuntu exemplo):
  ```bash
  sudo apt-get install git cmake build-essential libboost-all-dev \ 
       libglew-dev qtbase5-dev libeigen3-dev freeglut3-dev libsuitesparse-dev \ 
       libcgal-dev libceres-dev libfreeimage-dev libgoogle-glog-dev libgflags-dev \ 
       libsqlite3-dev libmetis-dev
  git clone https://github.com/colmap/colmap.git
  cd colmap
  mkdir build && cd build
  cmake .. -D CUDA_ENABLED=ON
  make -j$(nproc)
  sudo make install
  ```

> Em macOS com Apple Silicon: execução será CPU-only; considere reduzir número de imagens.

---
## 🧪 Dicas de Qualidade das Imagens
- Use fotos com sobreposição de 60–80%
- Varie ângulos e alturas
- Evite borrões e compressão excessiva
- Luz uniforme ajuda o detector de features

---
## 🛠 Possíveis Próximos Passos
- Visualização 3D direta no Streamlit (e.g. `pydeck` ou `trimesh` + `st.components`)
- Cache de resultados para não reprocessar o mesmo conjunto
- Suporte a vídeos (extraindo frames)
- Relatório automático com métricas (número de imagens, pontos, etc.)

---
## ❗ Troubleshooting
| Problema | Causa comum | Solução |
|----------|-------------|---------|
| `colmap: command not found` | COLMAP não instalado / PATH | Reinstale ou adicione ao PATH |
| Reconstrução vazia | Pouca sobreposição / imagens ruins | Recoletar melhor dataset |
| Processo muito lento | CPU-only + muitas imagens | Ativar CUDA ou reduzir imagens |
| `patch_match_stereo` falha | Diretórios incorretos | Confirmar `--workspace_path` e saída do undistorter |

---
## 📝 Licença
Defina aqui a licença (por exemplo MIT). *(Adapte conforme necessário.)*

---
## 🤝 Contribuições
Pull requests e sugestões são bem-vindos.
