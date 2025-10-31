from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware
from sqlalchemy.orm import Session
from ..db import get_db, init_db


async def on_startup() -> None:
	init_db()


async def health(request: Request) -> JSONResponse:
	return JSONResponse({"status": "ok"})


async def dcf(request: Request) -> JSONResponse:
	pair_id = request.path_params.get("pair_id", "")
	return JSONResponse(
		{
			"meta": {"model": "DCF"},
			"data": {
				"pair_id": pair_id,
				"enterprise_value": 0.0,
				"confidence": 0.0,
				"assumptions": {"note": "placeholder"},
				"provenance": {"source": "placeholder"},
			},
		}
	)


async def comps(request: Request) -> JSONResponse:
	pair_id = request.path_params.get("pair_id", "")
	return JSONResponse(
		{
			"meta": {"model": "Comps"},
			"data": {
				"pair_id": pair_id,
				"enterprise_value": 0.0,
				"confidence": 0.0,
				"assumptions": {"note": "placeholder"},
				"provenance": {"source": "placeholder"},
			},
		}
	)


routes = [
	Route("/health", endpoint=health),
	Route("/api/valuations/{pair_id}/dcf", endpoint=dcf),
	Route("/api/valuations/{pair_id}/comps", endpoint=comps),
]

middleware = [
	Middleware(GZipMiddleware, minimum_size=500),
	Middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_methods=["*"],
		allow_headers=["*"],
	),
]

app = Starlette(debug=False, routes=routes, on_startup=[on_startup], middleware=middleware)
