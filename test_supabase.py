from services.supabase_client import get_supabase_client


def main():
    try:
        client = get_supabase_client()
    except Exception as e:
        print("Erro ao criar cliente Supabase:", e)
        return

    try:
        payload = {
            "usuario": "teste_local",
            "acao": "teste_insercao",
            "descricao": "Teste de conexão via supabase-py",
            "ip": "127.0.0.1",
        }
        res = client.table("audit").insert(payload).execute()
        print("Resposta do Supabase:", res)
    except Exception as e:
        print("Falha ao inserir no Supabase:", e)


if __name__ == "__main__":
    main()
