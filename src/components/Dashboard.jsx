import React from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Upload } from "lucide-react";

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100 p-4 space-y-4">
      <h1 className="text-2xl font-bold text-center">Animal Biometrics Dashboard</h1>

      <Card className="p-4 shadow-xl rounded-2xl">
        <CardContent className="space-y-3">
          <h2 className="text-lg font-semibold">Registrar Animal</h2>
          <Input placeholder="Nombre" />
          <Input placeholder="Especie" />
          <Input placeholder="Raza" />
          <Button className="w-full">Guardar</Button>
        </CardContent>
      </Card>

      <Card className="p-4 shadow-xl rounded-2xl">
        <CardContent className="space-y-3">
          <h2 className="text-lg font-semibold">Registrar Huella</h2>
          <Input placeholder="ID del animal" />
          <Button className="w-full" variant="outline">
            <Upload className="w-4 h-4 mr-2" /> Subir Imagen
          </Button>
          <Button className="w-full">Registrar</Button>
        </CardContent>
      </Card>

      <Card className="p-4 shadow-xl rounded-2xl">
        <CardContent className="space-y-3">
          <h2 className="text-lg font-semibold">Verificar Huella</h2>
          <Button className="w-full" variant="outline">
            <Upload className="w-4 h-4 mr-2" /> Subir Imagen
          </Button>
          <Button className="w-full">Verificar</Button>
        </CardContent>
      </Card>
    </div>
  );
}
