# Gotchas - cada item daqui custou uma iteração real

## §1 · Fontes 120-240fps / 3400px+ → OOM e timeout
- `filter_complex` com vários `trim` do mesmo stream gigante = **OOM (Killed)**. Extraia cada segmento num comando ffmpeg separado (`-ss A -to B -i SRC` antes do input = seek rápido e frame-accurate com re-encode) e concatene depois.
- Vários encodes pesados num único comando bash = **timeout de execução**. Um encode pesado por chamada; os leves podem ir em lote.
- Jobs em background com `&` + `wait` no container não terminam de forma confiável. Rode sequencial.

## §2 · Concat: NUNCA `-c copy` entre segmentos encodados separadamente
ffmpeg decodifica e diz OK, mas **QuickTime/macOS rejeita** ("o arquivo não é compatível") por descontinuidade de timestamps. Sintoma real: "fui abrir o arquivo e deu erro". Solução: o passe final SEMPRE re-encoda (`-c:v libx264 -crf 18 -pix_fmt yuv420p -movflags +faststart`). Stream-copy só serve para intermediários que ainda vão passar por um re-encode.

## §3 · PNG em loop entra a 25fps por padrão
`-loop 1 -t 4.5 -i card.png` + `zoompan ... fps=30` ⇒ 4.5×25=113 frames declarados a 30fps = **3.77s** em vez de 4.5. A capa encolhe e desloca toda a cadeia de xfade. Solução: `-framerate 30` ANTES do `-loop 1 -i`.

## §4 · xfade: offsets com durações MEDIDAS, nunca nominais
Cada parte sai com ~1 frame a menos que o nominal (33ms). Em 14 fades o drift passa de 0.4s e a cadeia colapsa (sintoma: filme de 11s em vez de 113s). Antes de montar, `ffprobe` em cada parte e calcule `offset = cum_real - fade_dur`. Todas as partes precisam de mesmo tamanho/fps/pixfmt.

## §5 · Zoom animado
- `crop` NÃO aceita `t` em w/h (só em x/y) - "Error when evaluating the expression". Para zoom no tempo use `zoompan` com `z='1+(Z-1)*on/N'`, `d=1`, `s=WxH`, e clamps `x='max(0,min(iw-iw/zoom, CX-iw/zoom/2))'`.
- Zoom de fonte 1080p amolece texto de UI. Extraia o trecho do efeito a **2560×1440** da fonte original e deixe o zoompan descer para 1080p (`s=1920x1080`).

## §6 · Caixas de destaque × chat que rola
A linha destacada muda de Y conforme o chat streama. Caixa fixa o filme todo = caixa apontando para o nada. Solução: verifique UM frame (`-ss T -frames:v 1`), marque a caixa nesse layout e use `enable='between(t,T-1.5,T+2.5)'` relativo ao início do segmento. Pulso curto > caixa permanente.

## §7 · Coordenadas de efeito
Extraia o frame do intermediário JÁ normalizado e desenhe grade de 100px (PIL) antes de ler pixels. Aplicar drawbox ANTES do zoom (coordenadas no frame original; o zoom amplia a caixa junto).

## §8 · Cortes invisíveis
Corte sempre em tela estática (diff ~0 no detector). Verifique o frame de fronteira: erro que aparece em t=49 ⇒ cortar em ≤48.5; digitação do comando errado começa em t≈68 ⇒ cortar em ≤67. Final de gravação costuma ter frame preto - apare.

## §9 · Aspect ratios mistos na moldura
Rect da moldura = 1764×952 (em 1920×1080). 16:9 e 16:10: `scale=-2:952, pad=1764:952:(1764-iw)/2:0:color=white`. Ultrawide (~2.38): `scale=1764:-2, pad=1764:952:0:(952-ih)/2:color=white`. O pad branco some no tema claro do VS Code.

## §10 · Adobe Quick Cut
Exige A-roll (fala em câmera). Screen recording mudo ⇒ `StoryBuilderNoARoll`, sem retry que resolva. Também não corta por timestamp nem entende conteúdo de tela. Cheque trilha de áudio no ffprobe ANTES de propor; se a Paula invocou o Quick Cut, explique em 1 linha e siga com este pipeline.

## §11 · QA sempre, nos dois sentidos
Contact sheet do RESULTADO (não só das fontes) + `ffmpeg -v error -i out -f null -`. O sheet pega: LT fora de sincronia, destaque no lugar errado, erro que vazou, card curto. O decode-test pega arquivo quebrado - mas lembre: ele NÃO pega o problema do §2 (QuickTime é mais rígido que ffmpeg).
