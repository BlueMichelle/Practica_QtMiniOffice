# Documentación del Proceso de Firma de Código

## 1. Generación del Certificado
Se generó un certificado auto-firmado utilizando PowerShell:
```powershell
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=MiAppCert" -CertStoreLocation Cert:\CurrentUser\My
```

## 2. Exportación a PFX
El certificado se exportó a un archivo `.pfx` protegido por contraseña (contraseña usada en este ejemplo: `1234`):
```powershell
$password = ConvertTo-SecureString -String "1234" -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath "MiAppCert.pfx" -Password $password
```
Esto generó el archivo `MiAppCert.pfx` en el directorio del proyecto.

## 3. Firma del Ejecutable
Dado que `signtool` no estaba disponible en el PATH del sistema, se utilizó el cmdlet nativo de PowerShell `Set-AuthenticodeSignature` para firmar el ejecutable:
```powershell
$cert = Get-ChildItem Cert:\CurrentUser\My | Where-Object {$_.Subject -match "MiAppCert"} | Select-Object -First 1
Set-AuthenticodeSignature -FilePath dist\MiApp.exe -Certificate $cert
```

## 4. Verificación
Se verificó la firma utilizando:
```powershell
Get-AuthenticodeSignature dist\MiApp.exe
```
El resultado muestra `Status: Valid` (o `UnknownError` si el certificado raíz no es de confianza, lo cual es normal para certificados auto-firmados en la misma máquina si no se instalan en CA raíz).

También se puede verificar en las Propiedades del archivo -> Pestaña "Firmas digitales".

## Archivos Generados
- `MiAppCert.pfx`: Archivo del certificado exportado.
- `dist/MiApp.exe`: Ejecutable firmado.
