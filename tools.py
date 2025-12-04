from typing import Any
import httpx

# Constants
NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-app/1.0"

async def make_nws_request(url: str) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

def load_tools(mcp_server):
    @mcp_server.tool()
    async def hello(name: str) -> str:
        """
        Provides a hello world response for a username
    
        Args:
            name: "Bob"
        """
        return f"Hi {name}!" 
    
    @mcp_server.tool()
    async def get_forecast(latitude: float, longitude: float) -> str:
        """Get weather forecast for a location.
    
        Args:
        	latitude: Latitude of the location (recommended: up to 4 decimal places)
        	longitude: Longitude of the location (recommended: up to 4 decimal places)
        """
        # First get the forecast grid endpoint
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        points_data = await make_nws_request(points_url)
    
        if not points_data:
            return "Unable to fetch forecast data for this location."
    
        # Get the forecast URL from the points response
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await make_nws_request(forecast_url)
    
        if not forecast_data:
            return "Unable to fetch detailed forecast."
    
        # Format the periods into a readable forecast
        periods = forecast_data["properties"]["periods"]
        forecasts = []
        for period in periods[:5]:  # Only show next 5 periods
            forecast = f"""
    {period['name']}:
    Temperature: {period['temperature']}°{period['temperatureUnit']}
    Wind: {period['windSpeed']} {period['windDirection']}
    Forecast: {period['detailedForecast']}
    """
            forecasts.append(forecast)
    
        return "\n---\n".join(forecasts)
