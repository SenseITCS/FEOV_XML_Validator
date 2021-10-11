import Validator.AuxiliarFunctions

# Namespace necesario al momento de obtener un nodo, sin esto no se pueden leer los datos del nodo.
namespaces = {'eInvoiceNameSpace': 'https://cdn.comprobanteselectronicos.go.cr/xml-schemas/v4.3/facturaElectronica'}


def validateDetailsInfo(data):
    serviceDetailNode = data.find('eInvoiceNameSpace:DetalleServicio', namespaces)
    LineDetailsNodes = serviceDetailNode.findall('eInvoiceNameSpace:LineaDetalle', namespaces)
    lineNum = 0  # Contador de número de línea
    results = []
    for lineNode in LineDetailsNodes:
        results.append(validateLineNumber(lineNode, lineNum))
        results.append(validateLineCabysCode(lineNode, lineNum))
        results.append(validateCommercialCodeType(lineNode, lineNum))
        results.append(validateCommercialCodeCode(lineNode, lineNum))
        results.append(validateQty(lineNode, lineNum))
        results.append(validateUnitOfMeasure(lineNode, lineNum))
        results.append(validateComercialUnitOfMeasure(lineNode, lineNum))
        results.append(validateDetail(lineNode, lineNum))
        results.append(validateUnitPrice(lineNode, lineNum))
        results.append(validateTotalAmount(lineNode, lineNum))
        results.append(validateDiscount(lineNode, lineNum))
        results.append(validateDiscountReason(lineNode, lineNum))
        results.append(validateSubTotal(lineNode, lineNum))
        results.append(validateTaxBase(lineNode, lineNum))
        results.append(validateTaxCode(lineNode, lineNum))
        results.append(validateTaxRateCode(lineNode, lineNum))
        results.append(validateTaxRate(lineNode, lineNum))
        results.append(validateAmount(lineNode, lineNum))
        results.append(validateExonerationDocumentType(lineNode, lineNum))
        results.append(validateDocNumber(lineNode, lineNum))
        results.append(validateInstitutionName(lineNode, lineNum))
        results.append(validateSentDate(lineNode, lineNum))
        results.append(validateExemptionPercentage(lineNode, lineNum))
        results.append(validateExemptionAmount(lineNode, lineNum))
        results.append(validateNetTax(lineNode, lineNum))
        results.append(validateTotalLineAmount(lineNode, lineNum))
        results.append(validateOtherChargesDocuemntType(data, lineNum))
        results.append(validateThirdPartysName(data, lineNum))
        results.append(validateOCDetail(data, lineNum))
        results.append(validateOCPercent(data, lineNum))
        results.append(validateChargeAmount(data, lineNum))
        lineNum += 1

    formattedDetailResults = Validator.AuxiliarFunctions.flattenList(results)
    return formattedDetailResults


def validateLineNumber(data, lineNum):
    try:
        numLinea = data.find('eInvoiceNameSpace:NumeroLinea', namespaces).text
        if int(numLinea) < 1:
            return "Valor de nodo 'NumeroLinea' en sección DetalleServicio/LineaDetalle  no puede ser negativo. " \
                   "(LineaDetalle " + str(lineNum + 1) + ")"
        else:
            return True
    except:
        return "Valor de nodo 'NumeroLinea' no puede ser vacío."


def validateLineCabysCode(data, lineNum):
    try:
        cabysCode = data.find('eInvoiceNameSpace:Codigo', namespaces).text
        if len(cabysCode) != 13:
            return "Valor de nodo 'Codigo' en sección de DetalleServicio, línea " + str(
                lineNum + 1) + ", no posee un formato válido (13 caracteres. Recibido: " + cabysCode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateCommercialCodeType(data, LineNum):
    acceptedTypes = ["01", "02", "03", "04", "99"]
    try:
        commercialCodeNode = data.find('eInvoiceNameSpace:CodigoComercial', namespaces)
        commercialCodeType = commercialCodeNode.find('eInvoiceNameSpace:Tipo', namespaces).text
        if len(commercialCodeType) != 2 or commercialCodeType not in acceptedTypes:
            return "Valor (" + commercialCodeType + ") de nodo 'Tipo' en sección de DetalleServicio, línea " \
                   + str(LineNum + 1) + ",no es válido con respecto al catalogo de tipos: " + str(acceptedTypes)
        else:
            return True
    except:
        return "Valor de nodo 'Tipo' en sección 'DetalleServicio/LineaDetalle/CodigoComercial', no puede ser vacío."


def validateCommercialCodeCode(data, LineNum):
    try:
        commercialCodeNode = data.find('eInvoiceNameSpace:CodigoComercial', namespaces)
        commercialCodeCode = commercialCodeNode.find('eInvoiceNameSpace:Codigo', namespaces).text
        if len(commercialCodeCode) > 20:
            return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle/CodigoComercial', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (20 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle/CodigoComercial', no puede ser vacío."


def validateQty(data, LineNum):
    try:
        QtyNode = data.find('eInvoiceNameSpace:Cantidad', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(QtyNode, 13, 3)
        if not isValidDecimal:
            return "Valor de nodo 'Cantidad' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (13 enteros (máximo), 3 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'Cantidad' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateUnitOfMeasure(data, LineNum):
    try:
        UMNode = data.find('eInvoiceNameSpace:UnidadMedida', namespaces).text
        if len(UMNode) > 15:
            return "Valor de nodo 'UnidadMedida' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (máximo 15 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'UnidadMedida' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateComercialUnitOfMeasure(data, LineNum):
    try:
        comercialUMNode = data.find('eInvoiceNameSpace:UnidadMedidaComercial', namespaces).text
        if len(comercialUMNode) > 20:
            return "Valor de nodo 'UnidadMedidaComercial' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (máximo 20 caracteres)"
        else:
            return True
    except:
        return True


def validateDetail(data, LineNum):
    try:
        detailNode = data.find('eInvoiceNameSpace:Detalle', namespaces).text 
        if len(detailNode) > 200:
            return "Valor de nodo 'Detalle' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (máximo 200 caracteres. Recibido:" \
                   + str(len(detailNode)) + " caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'Detalle' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateUnitPrice(data, LineNum):
    try:
        unitPriceNode = data.find('eInvoiceNameSpace:PrecioUnitario', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(unitPriceNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'PrecioUnitario' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido ( 18 enteros (máximo), 5 decimales. Recibido: " \
                   + unitPriceNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'PrecioUnitario' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateTotalAmount(data, LineNum):
    try:
        totalAmountNode = data.find('eInvoiceNameSpace:MontoTotal', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(totalAmountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'MontoTotal' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido ( 18 enteros (máximo), 5 decimales. Recibido: " \
                   + totalAmountNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'MontoTotal' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateDiscount(data, LineNum):
    try:
        discountNode = data.find('eInvoiceNameSpace:Descuento', namespaces)
    except:
        return True
    try:
        discountAmountNode = discountNode.find('eInvoiceNameSpace:MontoDescuento', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(discountAmountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'MontoDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + discountAmountNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'MontoDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', no puede ser vacío."


def validateDiscountReason(data, LineNum):
    try:
        discountNode = data.find('eInvoiceNameSpace:Descuento', namespaces)
    except:
        return True
    try:
        discountReasonNode = discountNode.find('eInvoiceNameSpace:NaturalezaDescuento', namespaces).text
        if len(discountReasonNode) > 80:
            return "Valor de nodo 'NaturalezaDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (máximo 80 caracteres)"
        else:
            return True
    except:
        return "Valor de nodo 'NaturalezaDescuento' en sección 'DetalleServicio/LineaDetalle/Descuento', " \
               "no puede ser vacío."



def validateSubTotal(data, LineNum):
    try:
        subTotalNode = data.find('eInvoiceNameSpace:SubTotal', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(subTotalNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'SubTotal' en sección 'DetalleServicio/LineaDetalle', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + subTotalNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'SubTotal' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."


def validateTaxBase(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
        taxCode = taxNode.find('eInvoiceNameSpace:Codigo', namespaces).text
        if taxCode == "07":
            try:
                taxBaseNode = data.find('eInvoiceNameSpace:BaseImponible', namespaces).text
                isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(taxBaseNode, 18, 5)
                if not isValidDecimal:
                    return "Valor de nodo 'BaseImponible' en sección 'DetalleServicio/LineaDetalle', línea " \
                           + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. \
                            Recibido: "+ taxBaseNode + ")"
                else:
                    return True
            except:
                return "Valor de nodo 'BaseImponible' en sección 'DetalleServicio/LineaDetalle', no puede ser vacío."
        else:
            return True
    except:
        return True


def validateTaxCode(data, LineNum):
    acceptedCodes = ["01", "02", "03", "04", "05", "06", "07", "08", "12", "99"]
    # acceptedCodes = ["01", "02", "03", "04", "05", "06", "07", "08"]
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        taxCode = taxNode.find('eInvoiceNameSpace:Codigo', namespaces).text
        if len(taxCode) != 2 or taxCode not in acceptedCodes:
            return "Valor (" + taxCode +") de nodo 'Codigo' en sección DetalleServicio/LineaDetalle/Impuesto, línea "\
                   + str(LineNum + 1) + " no es válido con respecto al catalogo de tipos: " + str(acceptedCodes)
        else:
            return True
    except:
        return "Valor de nodo 'Codigo' en sección 'DetalleServicio/LineaDetalle/Impuesto', no puede ser vacío."


def validateTaxRateCode(data, LineNum):
    acceptedCodes = ["01", "02", "03", "04", "05", "06", "07", "08"]
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        taxRateCodNode = taxNode.find('eInvoiceNameSpace:CodigoTarifa', namespaces).text
        if len(taxRateCodNode) != 2 or taxRateCodNode not in acceptedCodes:
            return "Valor de nodo 'CodigoTarifa' en sección DetalleServicio/LineaDetalle/Impuesto, línea " \
                   + str(LineNum + 1) + " no posee un formato válido (2 caracteres) o no es válido con respecto " \
                   "al catalogo de tipos: " + str(acceptedCodes)
        else:
            return True
    except:
        return "Valor de nodo 'CodigoTarifa' en sección 'DetalleServicio/LineaDetalle/Impuesto', no puede ser vacío."


def validateTaxRate(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        taxRateNode = taxNode.find('eInvoiceNameSpace:Tarifa', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(taxRateNode, 4, 5)
        if not isValidDecimal:
            return "Valor de nodo 'Tarifa' en sección 'DetalleServicio/LineaDetalle/Impuesto', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: " \
                   + taxRateNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'Tarifa' en sección 'DetalleServicio/LineaDetalle/Impuesto', no puede ser vacío."


def validateAmount(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        amountNode = taxNode.find('eInvoiceNameSpace:Monto', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(amountNode, 18, 5)
        if not isValidDecimal:
            return "Valor de nodo 'Monto' en sección 'DetalleServicio/LineaDetalle/Impuesto', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales)"
        else:
            return True
    except:
        return "Valor de nodo 'Monto' en sección 'DetalleServicio/LineaDetalle/Impuesto/Monto', no puede ser vacío."


def validateExonerationDocumentType(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        exonerationNode = taxNode.find('eInvoiceNameSpace:Exoneracion', namespaces)
    except:
        return True
    acceptedTypes = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "99"]
    try:
        docTypeNode = exonerationNode.find('eInvoiceNameSpace:TipoDocumento', namespaces).text
        if len(docTypeNode) != 2 or docTypeNode not in acceptedTypes:
            return " Valor de nodo 'TipoDocumento' en sección DetalleServicio/LineaDetalle/Impuesto/Exoneracion," \
                   " línea " + str(LineNum + 1) + " no posee un formato válido (2 caracteres) o no es válido con" \
                   " respecto al catalogo de tipos: " + str(acceptedTypes)
        else:
            return True
    except:
        return "Valor de nodo 'TipoDocumento' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion', no " \
                       "puede ser vacío."


def validateDocNumber(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        exonerationNode = taxNode.find('eInvoiceNameSpace:Exoneracion', namespaces)
    except:
        return True
    try:
        docNum = exonerationNode.find('eInvoiceNameSpace:NumeroDocumento', namespaces).text
        if len(docNum) > 40:
            return " Valor de nodo 'NumeroDocumento' en sección 'DetalleServicio/LineaDetalle/Impuesto', línea " \
                   + str(LineNum + 1) + " no posee un formato válido (máximo 40 caracteres). "
        else:
            return True
    except:
        return "Valor de nodo 'NumeroDocumento' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion', " \
                   "no puede ser vacío."


def validateInstitutionName(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        exonerationNode = taxNode.find('eInvoiceNameSpace:Exoneracion', namespaces)
    except:
        return True
    try:
        instName = data.findall('eInvoiceNameSpace:NombreInstitucion', namespaces).text
        if len(instName) > 160:
            return " Valor de nodo 'NombreInstitucion' en sección 'DetalleServicio/LineaDetalle/Impuesto/" \
                   " Exoneracion/NombreInstitucion', línea " + str(LineNum + 1) + " no posee un formato válido" \
                   " (máximo 160 caracteres)."
        else:
            return True
    except:
        return "Valor de nodo 'NombreInstitucion' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion" \
               "/NombreInstitucion', no puede ser vacío."


def validateSentDate(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        exonerationNode = taxNode.find('eInvoiceNameSpace:Exoneracion', namespaces)
    except:
        return True
    try:
        dateNode = exonerationNode.find('eInvoiceNameSpace:FechaEmision', namespaces).text
        if dateNode:
            return True
    except:
        return "Valor de nodo 'FechaEmision' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion" \
                   "/FechaEmision', no puede ser vacío."


def validateExemptionPercentage(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        exonerationNode = taxNode.find('eInvoiceNameSpace:Exoneracion', namespaces)
    except:
        return True
    try:
        ExemptionNode = exonerationNode.find('eInvoiceNameSpace:PorcentajeExoneracion', namespaces).text
        if len(ExemptionNode) > 3:
            return "Valor de nodo 'PorcentajeExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/" \
                   "Exoneracion', línea " + str(LineNum + 1) + " no posee un formato válido (máximo 3 caracteres)."
        else:
            return True
    except:
        return "Valor de nodo 'PorcentajeExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/" \
               "Exoneracion, no puede ser vacío."


def validateExemptionAmount(data, LineNum):
    try:
        taxNode = data.find('eInvoiceNameSpace:Impuesto', namespaces)
    except:
        return True
    try:
        exonerationNode = taxNode.find('eInvoiceNameSpace:Exoneracion', namespaces)
    except:
        return True
    try:
        ExemptionAmountNode = exonerationNode.find('eInvoiceNameSpace:MontoExoneracion', namespaces).text
        isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(ExemptionAmountNode, 18, 5)
        if not isValidDecimal:
            return " Valor de nodo 'MontoExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion'," \
                   " línea " + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales." \
                   " Recibido: " + ExemptionAmountNode + ")"
        else:
            return True
    except:
        return "Valor de nodo 'MontoExoneracion' en sección 'DetalleServicio/LineaDetalle/Impuesto/Exoneracion" \
                   "/FechaEmision', no puede ser vacío."


def validateNetTax(data, LineNum):
    try:
        netTaxNode = data.find('eInvoiceNameSpace:ImpuestoNeto', namespaces)
        try:
            netTaxStr = netTaxNode.text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(netTaxStr, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo 'ImpuestoNeto' en sección 'DetalleServicio/LineaDetalle', línea " \
                       + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales. Recibido: "\
                       + netTaxStr + ")"
            else:
                return True
        except:
            return "Valor de nodo 'ImpuestoNeto' en sección 'DetalleServicio/LineaDetalle, no puede ser vacío."
    except:
        return "No se encuenta nodo 'ImpuestoNeto' en lineaDetalle " + LineNum + ", el cual es de caracter obligatorio."


def validateTotalLineAmount(data, LineNum):
    try:
        TLANode = data.find('eInvoiceNameSpace:MontoTotalLinea', namespaces)
        try:
            TLAStr = TLANode.text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(TLAStr, 18, 5)
            if not isValidDecimal:
                return "Valor de nodo 'MontoTotalLinea' en sección 'DetalleServicio/LineaDetalle', línea " \
                       + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales." \
                       " Recibido: " + TLAStr + ")"
            else:
                return True
        except:
            return "Valor de nodo 'MontoTotalLinea' en sección 'DetalleServicio/LineaDetalle, no puede ser vacío."
    except:
        return "No se encuenta nodo 'MontoTotalLinea' en lineaDetalle " + LineNum + ", el cual es de caracter" \
               " obligatorio."


def validateOtherChargesDocuemntType(data, LineNum):
    try:
        acceptedDocTypes = ["01", "02", "03", "04", "05", "06", "07", "99"]
        otherChargesNode = data.find('eInvoiceNameSpace:OtrosCargos', namespaces)
        try:
            OCDocTypeNode = otherChargesNode.find('eInvoiceNameSpace:TipoDocumento', namespaces).text
            if len(OCDocTypeNode) != 2 or OCDocTypeNode not in acceptedDocTypes:
                return " Valor de nodo 'TipoDocumento' en sección 'OtrosCargos', línea " + str(LineNum + 1) + \
                       " no posee un formato válido (2 caracteres) o no es válido con respecto" \
                       " al catalogo de tipos: " + str(acceptedDocTypes)
            else:
                return True
        except:
            return "Valor de nodo 'TipoDocumento' en sección './/OtrosCargos, no puede ser vacío."
    except:
        return True


def validateThirdPartysName(data, LineNum):
    try:
        otherChargesNode = data.find('eInvoiceNameSpace:OtrosCargos', namespaces)
        try:
            OCDocTypeNode = otherChargesNode.find('eInvoiceNameSpace:TipoDocumento', namespaces).text
            if OCDocTypeNode == "04":
                try:
                    nameNode = otherChargesNode.findall('eInvoiceNameSpace:NombreTercero', namespaces).text
                    if len(nameNode) > 100:
                        return " Valor de nodo 'NombreTercero' en sección 'OtrosCargos', línea " \
                               + str(LineNum + 1) + " no posee un formato válido (máximo 100 caracteres, caracteres" \
                               " recibidos: " + str(len(nameNode)) + ")"
                    else:
                        return True
                except:
                    return "Valor de nodo 'NombreTercero' en sección './/OtrosCargos, no puede ser vacío."
            else:
                return True
        except:
            return "Valor de nodo 'TipoDocumento' en sección './/OtrosCargos, no puede ser vacío."
    except:
        return True


def validateOCDetail(data, LineNum):
    try:
        otherChargesNode = data.find('eInvoiceNameSpace:OtrosCargos', namespaces)
        try:
            detailsNode = data.find('eInvoiceNameSpace:Detalle', namespaces).text
            if len(detailsNode) > 160:
                return " Valor de nodo 'Detalle' en sección 'OtrosCargos', línea " \
                       + str(LineNum + 1) + " no posee un formato válido (máximo 160 caracteres, caracteres" \
                       " recibidos: " + str(len(detailsNode)) + ")"
            else:
                return True
        except:
            return "Valor de nodo 'Detalle' en sección './/OtrosCargos, no puede ser vacío."
    except:
        return True


def validateOCPercent(data, LineNum):
    try:
        otherChargesNode = data.find('eInvoiceNameSpace:OtrosCargos', namespaces)
        try:
            percentageNode = otherChargesNode.find('eInvoiceNameSpace:Porcentaje', namespaces).text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(percentageNode, 9, 5)
            if not isValidDecimal:
                return " Valor de nodo 'Porcentaje' en sección 'OtrosCargos', línea " \
                       + str(LineNum + 1) + " no posee un formato válido (9 enteros (máximo), 5 decimales. Recibido: " \
                       + percentageNode + ")"
            else:
                return True
        except:
            return "Valor de nodo 'Porcentaje' en sección './/OtrosCargos, no puede ser vacío."
    except:
        return True


def validateChargeAmount(data, LineNum):
    try:
        otherChargesNode = data.find('eInvoiceNameSpace:OtrosCargos', namespaces)
        try:
            chargeNode = otherChargesNode.find('eInvoiceNameSpace:MontoCargo', namespaces).text
            isValidDecimal = Validator.AuxiliarFunctions.validateDecimal(chargeNode, 18, 5)
            if not isValidDecimal:
                return " Valor de nodo 'MontoCargo' en sección 'OtrosCargos', línea " \
                       + str(LineNum + 1) + " no posee un formato válido (18 enteros (máximo), 5 decimales." \
                       " Recibido: " + chargeNode + ")"
            else:
                return True
        except:
            return "Valor de nodo 'MontoCargo' en sección './/OtrosCargos, no puede ser vacío."
    except:
        return True
