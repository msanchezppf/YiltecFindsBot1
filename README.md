# 🤖 Bot de Discord — Buscador de Weidian

Bot que detecta fotos en Discord, las busca en dos tiendas de Weidian y
devuelve el enlace de HipoBuy con código de invitación.

---

## 📁 Estructura

```
discord-bot/
├── bot.py            ← Lógica principal del bot
├── weidian.py        ← Búsqueda por imagen y filtrado de tiendas
├── requirements.txt  ← Dependencias Python
├── .env.example      ← Plantilla de variables de entorno
└── README.md
```

---

## ⚙️ Configuración paso a paso

### 1. Crear el bot en Discord

1. Ve a https://discord.com/developers/applications
2. Haz clic en **New Application** → ponle nombre → **Create**
3. En el menú lateral ve a **Bot** → **Add Bot** → confirma
4. En la sección **Privileged Gateway Intents** activa:
   - ✅ **Message Content Intent**
5. Haz clic en **Reset Token** → copia el token (solo se muestra una vez)
6. Ve a **OAuth2 → URL Generator**:
   - Scopes: `bot`
   - Bot Permissions: `Send Messages`, `Read Message History`, `View Channels`
7. Copia la URL generada → ábrela en el navegador → añade el bot a tu servidor

### 2. Configurar variables de entorno

```bash
cp .env.example .env
```

Edita `.env` y pega tu token:
```
DISCORD_TOKEN=MTxxxxxxxxxxxxxxxxxxxxxxxx.Gxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Python 3.10+** recomendado.

### 4. (Opcional) Restringir canales

En `bot.py`, edita la línea:
```python
ALLOWED_CHANNELS: set[int] = set()
```

Para permitir solo canales concretos:
```python
ALLOWED_CHANNELS: set[int] = {123456789012345678, 987654321098765432}
```
Los IDs los obtienes haciendo clic derecho sobre el canal en Discord (con modo desarrollador activado).

### 5. Arrancar el bot

```bash
python bot.py
```

Verás en consola:
```
✅ Bot conectado como TuBot#1234 (ID: 123456789)
🔍 Listo para buscar productos en Weidian
```

---

## 🚀 Funcionamiento

| Situación | Respuesta del bot |
|-----------|-------------------|
| Producto en ambas tiendas | Enlace de tienda 1 + enlace de tienda 2 |
| Producto solo en tienda 1 | Solo enlace de tienda 1 |
| Producto solo en tienda 2 | Solo enlace de tienda 2 |
| No encontrado en ninguna | "No lo encuentro, avisa a Mario y él te lo encontrará." |

### Formato del enlace generado

```
https://hipobuy.com/product/weidian/{ID_PRODUCTO}?inviteCode=8DDUA6VFZ
```

---

## 🔧 Tiendas configuradas

| Tienda | User ID |
|--------|---------|
| Tienda 1 | 1744208227 |
| Tienda 2 | 1789446587 |

Para cambiar las tiendas edita `weidian.py`:
```python
STORE_1_USER_ID = "1744208227"
STORE_2_USER_ID = "1789446587"
```

---

## 🌐 Mantenerlo activo 24/7

### Opción A — Railway (gratis/barato)
1. Sube el código a un repositorio de GitHub (privado)
2. Ve a https://railway.app → **New Project → Deploy from GitHub**
3. Añade la variable de entorno `DISCORD_TOKEN` en la sección **Variables**
4. Railway desplegará y mantendrá el bot activo

### Opción B — VPS / Servidor propio
```bash
# Con screen
screen -S discord-bot
python bot.py
# Ctrl+A, D para dejar en segundo plano

# O con systemd (más robusto)
```

---

## ⚠️ Nota importante

Weidian no tiene una API pública de búsqueda visual documentada.
El bot usa los endpoints internos que utiliza la app de Weidian.
Si Weidian cambia su API, puede ser necesario actualizar `weidian.py`.

En ese caso, otra opción es usar **SerpAPI** (Google Lens) para identificar
el producto y luego buscarlo en las tiendas. Contacta si necesitas esa variante.

---

## 📝 Comandos adicionales

| Comando | Descripción |
|---------|-------------|
| `!ping` | Comprueba que el bot responde |

---

**Código de invitación HipoBuy:** `8DDUA6VFZ`
