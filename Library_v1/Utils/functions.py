import asyncio
import sys

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def run_async(fn):
    try:
        # Verifica se o loop de eventos já está rodando
        loop = asyncio.get_event_loop()
        if loop.is_running():
            print("Reutilizando o loop de eventos existente.")
            loop.create_task(fn())  # Cria a tarefa no loop existente
        else:
            asyncio.run(fn())  # Se o loop não estiver rodando, cria um novo
    except RuntimeError as e:
        raise RuntimeError(e)

async def run_async_wait_event():
    await asyncio.Event().wait()

def run_until_complete(task: callable):
    try:
        # Obtém o loop de eventos atual ou cria um novo
        try:
            loop = asyncio.get_event_loop()
            if not loop.is_running():
                return loop.run_until_complete(task())
        except RuntimeError:
            # Caso não exista um loop, cria um novo
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(task())
    except RuntimeError as e:
        raise RuntimeError(f"Erro ao executar função assíncrona: {e}")
    finally:
        if 'loop' in locals() and loop.is_closed():
            loop.close()