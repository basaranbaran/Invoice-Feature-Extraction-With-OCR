import fs from 'fs'
import axios from 'axios'
import FormData from 'form-data'
import { PrismaClient } from '@prisma/client'

const prisma = new PrismaClient()

export const uploadInvoice = async (req, res) => {
  try {
    if (!req.user) return res.status(401).json({ error: 'Unauthorized' })

    const form = new FormData()
    form.append('file', fs.createReadStream(req.file.path), req.file.originalname)
    form.append('model', req.body.model || 'llama3.1:latest')
    form.append('docType', req.body.docType || 'fatura')

    const response = await axios.post('http://localhost:8000/extract-invoice', form, {
      headers: form.getHeaders()
    })

    const invoice = await prisma.invoice.create({
      data: {
        filename: req.file.originalname,
        imagePath: req.file.path,
        parsedData: response.data,
        userId: req.user.id,
      },
    })

    res.json(invoice)
  } catch (err) {
    console.error('Backend error:', err)
    res.status(500).json({ error: 'Fatura yükleme başarısız', detail: err.message })
  }
}

export const getInvoiceById = async (req, res) => {
  try {
    const invoice = await prisma.invoice.findUnique({
      where: { id: parseInt(req.params.id) }
    })

    if (!invoice || invoice.userId !== req.user?.id) {
      return res.status(404).json({ error: 'Invoice not found' })
    }

    res.json(invoice)
  } catch (err) {
    console.error('getInvoiceById error:', err)
    res.status(500).json({ error: 'Fatura alınamadı' })
  }
}

export const listInvoices = async (req, res) => {
  try {
    if (!req.user) return res.status(401).json({ error: 'Unauthorized' })

    const invoices = await prisma.invoice.findMany({
      where: { userId: req.user.id },
      orderBy: { createdAt: 'desc' },
    })

    res.json(invoices)
  } catch (err) {
    console.error('listInvoices error:', err)
    res.status(500).json({ error: 'Faturalar listelenemedi' })
  }
}
  