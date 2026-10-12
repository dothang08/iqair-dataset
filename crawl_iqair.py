from playwright.sync_api import sync_playwright
import json
from datetime import datetime
import csv
import pathlib
from zoneinfo import ZoneInfo
from typing import Dict, Optional
import re

# Define cities data
CITIES = [
    {
        "name": "hanoi",
        "display_name": "Hà Nội",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/ha-noi/hanoi"
    },
    {
        "name": "ho-chi-minh-city",
        "display_name": "Hồ Chí Minh",
        "url": "https://www.iqair.com/vi/vietnam/ho-chi-minh-city/ho-chi-minh-city"
    },
    {
        "name": "da-nang",
        "display_name": "Đà Nẵng",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/da-nang-city/da-nang"
    },
    {
        "name": "hai-phong",
        "display_name": "Hải Phòng",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/hai-phong-city/haiphong"
    },
    {
        "name": "nha-trang",
        "display_name": "Nha Trang",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/khanh-hoa/nha-trang"
    },
    {
        "name": "can-tho",
        "display_name": "Cần Thơ",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/thanh-pho-can-tho/can-tho"
    },
    {
        "name": "hue",
        "display_name": "Huế",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/tinh-thua-thien-hue/hue"
    },
    {
        "name": "thai-nguyen",
        "display_name": "Thái Nguyên",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/tinh-thai-nguyen/thai-nguyen"
    },
    {
        "name": "bac-ninh",
        "display_name": "Bắc Ninh",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/bac-ninh/bac-ninh"
    },
    {
        "name": "tra-vinh",
        "display_name": "Trà Vinh",
        "url": "https://www.iqair.com/vi/air-quality/vietnam/tinh-tra-vinh/tra-vinh"
    }
]

# Lấy thời gian hiện tại ở múi giờ Việt Nam (GMT+7)
def get_vietnam_time():
    """Get current time in Vietnam timezone (GMT+7)"""
    return datetime.now(ZoneInfo("Asia/Bangkok"))

# Xác thực dữ liệu AQI
def validate_aqi(aqi: str) -> Optional[str]:
    """Validate AQI value"""
    try:
        aqi_value = int(re.sub(r'\D', '', aqi))
        if 0 <= aqi_value <= 500:
            return str(aqi_value)
    except (ValueError, TypeError):
        pass
    return None

# Xác thực dữ liệu wind speed
def validate_wind_speed(speed: str) -> Optional[str]:
    """Validate wind speed"""
    try:
        if re.match(r'^\d+(\.\d+)?\s*(km/h|mph)$', speed.strip()):
            speed = speed.strip()
            if 'mph' in speed:
                value = float(re.match(r'^\d+(\.\d+)?', speed).group())
                km_value = value * 1.60934
                return f"{km_value:.1f} km/h"
            return speed
    except (ValueError, TypeError, AttributeError):
        pass
    return None

# Xác thực dữ liệu humidity
def validate_humidity(humidity: str) -> Optional[str]:
    """Validate humidity"""
    try:
        if re.match(r'^\d{1,3}%$', humidity.strip()):
            return humidity.strip()
    except (ValueError, TypeError, AttributeError):
        pass
    return None

# Xác thực dữ liệu temperature
def validate_temperature(temp: str) -> Optional[str]:
    """Validate temperature value (convert from Fahrenheit to Celsius if needed)"""
    try:
        temp_value = float(re.sub(r'[^\d.-]', '', temp))
        if temp_value > 50:
            temp_value = (temp_value - 32) * 5 / 9
        if -50 <= temp_value <= 50:
            return f"{temp_value:.1f}°C"
    except (ValueError, TypeError):
        pass
    return None

# Xác thực dữ liệu pollutant
def validate_pollutant(value: str) -> Optional[str]:
    """Validate pollutant value"""
    try:
        cleaned_value = re.sub(r'[^\d.]', '', value)
        if not cleaned_value:
            return None
        value_float = float(cleaned_value)
        if 0 <= value_float <= 10000:
            return f"{value_float:.1f}"
    except (ValueError, TypeError):
        pass
    return None

# Crawl data for a specific city
def crawl_city_data(page, city: Dict) -> Optional[Dict]:
    """Crawl data for a specific city"""
    print(f"\nAccessing {city['display_name']} ({city['url']})...")

    try:
        page.goto(city['url'], wait_until="domcontentloaded", timeout=60000)

        body_text = ""
        for attempt in range(3):
            page.wait_for_timeout(5000)
            body_text = page.locator("body").inner_text(timeout=10000)

            if "AQI" in body_text and "Dự báo theo giờ" in body_text:
                break

            print(f"Waiting for data... attempt {attempt + 1}/3")

        text = re.sub(r'\s+', ' ', body_text)
        current_section = text.split("Dự báo theo giờ")[0]

        # AQI
        aqi_match = re.search(
            r'(\d{1,3})\*?\s+AQI⁺?\s*MỸ',
            current_section,
            re.IGNORECASE
        )
        aqi = validate_aqi(aqi_match.group(1)) if aqi_match else None

        if aqi is None:
            print(f"No valid AQI found for {city['display_name']}")
            return None

        # Temperature
        temp_match = re.search(r'(-?\d+(?:\.\d+)?)°', current_section)
        temperature = validate_temperature(temp_match.group(1)) if temp_match else None

        # Wind speed
        wind_match = re.search(r'(\d+(?:\.\d+)?)\s*km/h', current_section)
        wind_speed = validate_wind_speed(f"{wind_match.group(1)} km/h") if wind_match else None

        # Humidity
        humidity_match = re.search(r'(\d{1,3})\s*%', current_section)
        humidity = validate_humidity(f"{humidity_match.group(1)}%") if humidity_match else None

        pollutant_data = {
            "pm25": "N/A",
            "pm10": "N/A",
            "o3": "N/A",
            "no2": "N/A",
            "so2": "N/A",
            "co": "N/A"
        }

        if "Chất gây ô nhiễm không khí" in text:
            pollutant_section = text.split("Chất gây ô nhiễm không khí", 1)[1]

            if "Nồng độ PM2.5 hiện tại" in pollutant_section:
                pollutant_section = pollutant_section.split("Nồng độ PM2.5 hiện tại", 1)[0]

            # Thông tin về các chất gây ô nhiễm
            pollutant_patterns = {
                "pm25": r'PM2\.5.*?(\d+(?:\.\d+)?)\s*\*?\s*µg/m³',
                "pm10": r'PM10.*?(\d+(?:\.\d+)?)\s*\*?\s*µg/m³',
                "o3": r'O₃.*?(\d+(?:\.\d+)?)\s*\*?\s*µg/m³',
                "no2": r'NO₂.*?(\d+(?:\.\d+)?)\s*\*?\s*µg/m³',
                "so2": r'SO₂.*?(\d+(?:\.\d+)?)\s*\*?\s*µg/m³',
                "co": r'CO.*?(\d+(?:\.\d+)?)\s*\*?\s*µg/m³'
            }

            for key, pattern in pollutant_patterns.items():
                match = re.search(pattern, pollutant_section, re.IGNORECASE)
                if match:
                    value = validate_pollutant(match.group(1))
                    if value is not None:
                        pollutant_data[key] = value

        print("AQI:", aqi)
        print("Temperature:", temperature)
        print("Wind speed:", wind_speed)
        print("Humidity:", humidity)
        print("Pollutants:", pollutant_data)

        return {
            "timestamp": get_vietnam_time().isoformat(),
            "city": city['display_name'],
            "aqi": aqi,
            "wind_speed": wind_speed,
            "humidity": humidity,
            "temperature": temperature,
            **pollutant_data
        }

    except Exception as e:
        print(f"Error extracting data for {city['display_name']}: {str(e)}")
        return None


def save_to_csv(data: Dict, city_name: str):
    """Save data to CSV file for a specific city"""
    now = get_vietnam_time()
    result_dir = pathlib.Path(f"result/{city_name}")
    result_dir.mkdir(parents=True, exist_ok=True)
    filename = f"aqi_{city_name}_{now.year}_{now.strftime('%b').lower()}.csv"
    filepath = result_dir / filename
    headers = ["timestamp", "city", "aqi", "wind_speed", "humidity", "temperature", "pm25", "pm10", "o3", "no2", "so2", "co"]
    file_exists = filepath.exists()

    with open(filepath, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

    return filepath


def crawl_all_cities():
    """Crawl data for all cities"""
    results = []

    for city in CITIES:
        print(f"\n{'='*50}")
        print(f"Processing {city['display_name']}...")

        try:
            with sync_playwright() as p:
                try:
                    browser = p.chromium.launch(headless=True)
                    page = browser.new_page()
                    page.set_viewport_size({"width": 1280, "height": 720})
                    page.set_default_timeout(60000)
                    page.set_default_navigation_timeout(60000)

                    data = crawl_city_data(page, city)

                    if data:
                        results.append(data)
                        csv_file = save_to_csv(data, city['name'])
                        print(f"Data saved to: {csv_file}")
                    else:
                        print(f"Skipping invalid data for {city['display_name']}")

                except Exception as e:
                    print(f"Browser error for {city['display_name']}: {str(e)}")
                    continue

                finally:
                    if 'browser' in locals():
                        browser.close()

        except Exception as e:
            print(f"Playwright error for {city['display_name']}: {str(e)}")
            continue

    return results


if __name__ == "__main__":
    try:
        print("Starting IQAir data crawler...")
        print(f"Current time in Vietnam: {get_vietnam_time().strftime('%Y-%m-%d %H:%M:%S %Z')}")

        results = crawl_all_cities()

        print("\nCrawled data:")
        print(json.dumps(results, indent=2, ensure_ascii=False))

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        raise e
