# -*- coding: utf-8 -*-

######
# Programa realizado en ubuntu con python 2.7.6
# Autor: José María Fernández Campos
######

import MySQLdb
from gi.repository import Gtk
import os
import time

# Establecemos la conexión a la Base de datos (variables globales)
Conexion = MySQLdb.connect(host='localhost', user='conan', passwd='crom', db='Noticias')
micursor = Conexion.cursor(MySQLdb.cursors.DictCursor)


class Handler:
	builder=None
	def __init__(self):
		# Iniciamos el GtkBuilder para tirar del fichero de glade
		self.builder = Gtk.Builder()
		self.builder.add_from_file("noticias.glade")
		self.handlers = {
			"onRecopilarActivate": self.onRecopilarActivate,		# Opciones del menú
			"onConsultarActivate": self.onConsultarActivate,
			"on_btn_recopilar_clicked": self.on_btn_recopilar_clicked,	# Clic en botón
			"on_btn_consultar_clicked": self.on_btn_consultar_clicked,
			"onSelectAboutDialog": self.onSelectAboutDialog,	# About
			"onCloseAboutDialog": self.onCloseAboutDialog,
			"onDeleteWindow": self.onDeleteWindow			# Cerrar
		}
		
		# Conectamos las señales e iniciamos la aplicación
		self.builder.connect_signals(self.handlers)
		self.window = self.builder.get_object("window")
		self.about = self.builder.get_object("aboutdialog")
		self.btn_recopilar = self.builder.get_object("btn_recopilar")	# Botones
		self.btn_consultar = self.builder.get_object("btn_consultar")
		self.enlace1 = self.builder.get_object("enlace1")			# Texto y enlaces de noticias
		self.enlace2 = self.builder.get_object("enlace2")
		self.enlace3 = self.builder.get_object("enlace3")
		self.enlace4 = self.builder.get_object("enlace4")
		self.enlace5 = self.builder.get_object("enlace5")
		self.mensaje = self.builder.get_object("mensaje")			# Mensaje de texto para el usuario
		self.comboboxtext_fecha = self.builder.get_object("comboboxtext_fecha")  # Selección de fecha
		self.sel_fecha = self.builder.get_object("sel_fecha")
		self.spinner = self.builder.get_object("spinner")

		self.fechas = []				# Si hay fechas anteriores, inicializar el combobox para seleccionarlas
		query = "SELECT DISTINCT Fecha FROM Noticias;"
		micursor.execute(query)
		registros = micursor.fetchall()

		for r in registros:
			self.fechas.append(r['Fecha'])
			self.comboboxtext_fecha.append_text(r['Fecha'])

		self.window.show_all()
		self.btn_recopilar.hide()
		self.btn_consultar.hide()
		self.enlace1.hide()
		self.enlace2.hide()
		self.enlace3.hide()
		self.enlace4.hide()
		self.enlace5.hide()
		self.sel_fecha.hide()
		self.spinner.hide()
		self.comboboxtext_fecha.hide()
		self.window.resize(1000,200)

	# Al seleccionar opción en el menú, solo mostramos el botón indicado
	def onRecopilarActivate(self, *args):
		self.btn_recopilar.show()
		self.btn_consultar.hide()
		self.mensaje.hide()
		self.sel_fecha.hide()
		self.comboboxtext_fecha.hide()

	def onConsultarActivate(self, *args):
		self.btn_recopilar.hide()
		self.btn_consultar.show()
		self.mensaje.hide()
		self.sel_fecha.show()
		self.comboboxtext_fecha.show()


	# --- Al hacer clic en un botón ---
	# RECOPILAR
	def on_btn_recopilar_clicked(self, *args):
		fecha_hoy = ''

		# Si hay ya noticias de hoy, borrarlas
		now = time.strftime("%d.%m.%Y")
		query = "DELETE FROM Noticias WHERE Fecha = '"+now+"';"
		micursor.execute(query)
		Conexion.commit()

		# Ejecutamos araña
		self.spinner.show()
		self.spinner.start()
		os.system("scrapy crawl NoticiasSpider")
		self.spinner.stop()
		self.spinner.hide()

		# scrapy debe haber almacenado en la DB las noticias con fecha de hoy
		query = "SELECT * FROM Noticias WHERE Fecha LIKE '" +now+ "%';"
		micursor.execute(query)

		noticia1 = micursor.fetchone()
		if noticia1 is not None:				# Normalmente hay más de 5 noticias, pero por si acaso
			fecha_hoy = noticia1['Fecha']		# Si hay resultados, añadir esta fecha al combobox (al final)
			self.enlace1.set_label(noticia1['Titulo'])
			self.enlace1.set_uri(noticia1['Enlace'])
			self.enlace1.show()

		noticia = micursor.fetchone()
		if noticia is not None:
			self.enlace2.set_label(noticia['Titulo'])
			self.enlace2.set_uri(noticia['Enlace'])
			self.enlace2.show()

		noticia = micursor.fetchone()
		if noticia is not None:
			self.enlace3.set_label(noticia['Titulo'])
			self.enlace3.set_uri(noticia['Enlace'])
			self.enlace3.show()

		noticia = micursor.fetchone()
		if noticia is not None:
			self.enlace4.set_label(noticia['Titulo'])
			self.enlace4.set_uri(noticia['Enlace'])
			self.enlace4.show()

		noticia = micursor.fetchone()
		if noticia is not None:
			self.enlace5.set_label(noticia['Titulo'])
			self.enlace5.set_uri(noticia['Enlace'])
			self.enlace5.show()

		if fecha_hoy is not '' and fecha_hoy not in self.fechas:		# Si en el combobox no está la fecha de hoy, se añade
			self.fechas.append(noticia1['Fecha'])
			self.comboboxtext_fecha.append_text(fecha_hoy)

		self.mensaje.set_text("Noticias existentes recogidas satisfactoriamente.")
		self.mensaje.show()

	# CONSULTAR
	def on_btn_consultar_clicked(self, *args):
		fecha_seleccionada = self.comboboxtext_fecha.get_active_text()

		if fecha_seleccionada is not None:		# Si se ha seleccionado fecha, ejecutar select y mostrar
			query = "SELECT * FROM Noticias WHERE Fecha=\""+fecha_seleccionada+"\";"
			micursor.execute(query)

			noticia1 = micursor.fetchone()
			if noticia1 is not None:
				fecha_hoy = noticia1['Fecha']
				self.enlace1.set_label(noticia1['Titulo'])
				self.enlace1.set_uri(noticia1['Enlace'])
				self.enlace1.show()

			noticia = micursor.fetchone()
			if noticia is not None:
				self.enlace2.set_label(noticia['Titulo'])
				self.enlace2.set_uri(noticia['Enlace'])
				self.enlace2.show()

			noticia = micursor.fetchone()
			if noticia is not None:
				self.enlace3.set_label(noticia['Titulo'])
				self.enlace3.set_uri(noticia['Enlace'])
				self.enlace3.show()

			noticia = micursor.fetchone()
			if noticia is not None:
				self.enlace4.set_label(noticia['Titulo'])
				self.enlace4.set_uri(noticia['Enlace'])
				self.enlace4.show()

			noticia = micursor.fetchone()
			if noticia is not None:
				self.enlace5.set_label(noticia['Titulo'])
				self.enlace5.set_uri(noticia['Enlace'])
				self.enlace5.show()

			self.mensaje.set_text("Noticias existentes mostradas satisfactoriamente.")
		else:
			self.mensaje.set_text("Debe seleccionar una fecha.")
		self.mensaje.show()

	def onDeleteWindow(self, *args):
		# Borrar el contenido de la base de datos
		#query = "DELETE FROM Noticias WHERE 1;"
		#micursor.execute(query)
		#Conexion.commit()

		# Cerramos DB
		micursor.close()
		Conexion.close()

		Gtk.main_quit(*args)

	def onSelectAboutDialog(self, *args):
		self.about.show()

	def onCloseAboutDialog(self, window, data=None):
		self.about.hide()


def main():
	window = Handler()
	Gtk.main()
	return 0

if __name__ == '__main__':
	main()


