# Importando libs
# stdlib imports
from os import environ as env
from datetime import datetime

# 3rd party imports
import aiohttp
from fastapi.logger import logger
from fastapi.responses import JSONResponse
from fastapi import status, HTTPException
from bs4 import BeautifulSoup

# Local imports
from src.models import *
from utils.util import get_headers

# Captura variáveis de ambiente e cria constantes
TIMEOUT = env.get('TIMEOUT', default=180)

# Fazendo o parser
async def parse(soup):
    table = soup.find('table')
    if not table:
        raise HTTPException(status_code=404, detail="Table not found")

    # Captura os cabeçalhos e subcabeçalhos da tabela
    diseases = ["PARALISIA FLÁCIDA AGUDA", "SARAMPO", "RUBÉOLA", "CORONA VÍRUS"]
    
    data = []
    tbody = table.find('tbody')
    for row in tbody.find_all('tr'):
        columns = row.find_all('td')
        hospital_name = columns[0].text.strip()
        
        hospital_data = {"nome_hospital": hospital_name, "doencas": []}
        
        # Organiza os dados por doenças e status
        for i, disease in enumerate(diseases):
            base_index = 1 + i * 3
            disease_data = {
                "nome_doenca": disease,
                "positivo": columns[base_index].text.strip(),
                "negativo": columns[base_index + 1].text.strip(),
                "silenciado": columns[base_index + 2].text.strip()
            }
            hospital_data["doencas"].append(disease_data)
        
        data.append(hospital_data)
    
    return data
#-----------------------------------------------------------------------------------------------------
async def fetch(ano: int):
    if not ano:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"code": 422, "message": "Unprocessable Entity",
                     "datetime": datetime.now().isoformat()}
        )
    
    
    

    # Configura os timeouts
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        # Configurando headers
        session.headers.update(get_headers())
        session.headers.update({'Host': 'simda.sms.fortaleza.ce.gov.br'})

        try:
            
            url = f'https://simda.sms.fortaleza.ce.gov.br/simda/notificacao-negativa/tabela-semana?agravo=&ano={ano}&modo=estabelecimento'

            async with session.get(url, ssl=False, allow_redirects=True) as resp:
                logger.debug(f"Consulta: {resp.status} - {url}")
                resp_content = await resp.read()
                soup = BeautifulSoup(resp_content, 'html.parser')
                
                # Faz o parse do conteudo
                result = await parse(soup)
                
                
                
        except aiohttp.ClientError as e:
            logger.exception('Erro durante a consulta API')
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    'code': 500,
                    'message': f'INTERNAL_SERVER_ERROR: {str(e)}'
                }
            )
        except Exception as e:
            logger.exception('Erro inesperado durante a consulta API')
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    'code': 500,
                    'message': f'INTERNAL_SERVER_ERROR: {str(e)}'
                }
            )

        logger.info(f"Consulta finalizada: {result}")
        return result
