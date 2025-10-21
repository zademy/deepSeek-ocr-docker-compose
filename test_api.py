#!/usr/bin/env python3
"""
Script de prueba para el API de DeepSeek OCR
"""

import requests
import sys
import time
from pathlib import Path


API_URL = "http://localhost:8000"


def test_health():
    """Verificar salud del API"""
    print("🏥 Verificando salud del API...")
    try:
        response = requests.get(f"{API_URL}/health", timeout=5)
        data = response.json()
        
        if data.get("status") == "healthy":
            print("✅ API está saludable")
            print(f"   - Modelo cargado: {data.get('model_loaded')}")
            print(f"   - Device: {data.get('device')}")
            print(f"   - CUDA disponible: {data.get('cuda_available')}")
            return True
        else:
            print("❌ API no está saludable")
            return False
    except Exception as e:
        print(f"❌ Error conectando al API: {e}")
        return False


def test_modes():
    """Obtener modos disponibles"""
    print("\n📋 Obteniendo modos disponibles...")
    try:
        response = requests.get(f"{API_URL}/api/modes", timeout=5)
        modes = response.json()
        
        print("✅ Modos disponibles:")
        for mode, info in modes.get("modes", {}).items():
            print(f"\n   {mode}:")
            print(f"   - {info['description']}")
            print(f"   - Velocidad: {info['speed']}")
            print(f"   - Uso: {info['use_case']}")
        return True
    except Exception as e:
        print(f"❌ Error obteniendo modos: {e}")
        return False


def test_ocr(image_path, mode="markdown"):
    """Probar OCR con una imagen"""
    print(f"\n🖼️  Probando OCR con imagen: {image_path}")
    print(f"   Modo: {mode}")
    
    if not Path(image_path).exists():
        print(f"❌ Archivo no encontrado: {image_path}")
        return False
    
    try:
        with open(image_path, 'rb') as f:
            files = {'file': f}
            data = {'mode': mode}
            
            print("   ⏳ Procesando...")
            start = time.time()
            
            response = requests.post(
                f"{API_URL}/api/ocr",
                files=files,
                data=data,
                timeout=300  # 5 minutos máximo
            )
            
            elapsed = time.time() - start
            
            if response.ok:
                result = response.json()
                print(f"✅ OCR completado en {result['processing_time']}s")
                print(f"   - Tamaño imagen: {result['image_size']}")
                print(f"   - Modo usado: {result['mode']}")
                print(f"\n   📄 Texto extraído (primeros 200 chars):")
                print(f"   {result['text'][:200]}...")
                return True
            else:
                print(f"❌ Error en OCR: {response.status_code}")
                print(f"   {response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error procesando OCR: {e}")
        return False


def run_tests(image_path=None):
    """Ejecutar todas las pruebas"""
    print("=" * 60)
    print("🧪 Iniciando pruebas de DeepSeek OCR API")
    print("=" * 60)
    
    results = {}
    
    # Test 1: Health check
    results['health'] = test_health()
    
    if not results['health']:
        print("\n❌ API no está disponible. Asegúrate de que esté corriendo:")
        print("   docker-compose up -d")
        return False
    
    # Test 2: Modos
    results['modes'] = test_modes()
    
    # Test 3: OCR (si se proporciona imagen)
    if image_path:
        results['ocr'] = test_ocr(image_path)
    else:
        print("\n⚠️  No se proporcionó imagen para prueba de OCR")
        print("   Uso: python test_api.py <ruta_imagen>")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 Resumen de pruebas:")
    print("=" * 60)
    
    for test, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test}")
    
    all_passed = all(results.values())
    
    if all_passed:
        print("\n🎉 Todas las pruebas pasaron exitosamente!")
    else:
        print("\n⚠️  Algunas pruebas fallaron. Revisa los logs arriba.")
    
    return all_passed


if __name__ == "__main__":
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    success = run_tests(image_path)
    sys.exit(0 if success else 1)
