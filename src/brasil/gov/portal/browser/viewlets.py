# -*- coding: utf-8 -*-
""" Modulo que implementa os viewlets do Portal Modelo"""
from brasil.gov.portal.config import REDES
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ServicosViewlet(ViewletBase):
    ''' Viewlet de listagem de servicos
    '''
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/servicos.pt')

    def update(self):
        ''' Prepara/Atualiza os valores utilizados pelo Viewlet
        '''
        super(ServicosViewlet, self).update()
        ps = self.context.restrictedTraverse('@@plone_portal_state')
        tools = self.context.restrictedTraverse('@@plone_tools')
        portal = ps.portal()
        self._folder = 'servicos' in portal.objectIds() and portal['servicos']
        self._ct = tools.catalog()

    def available(self):
        return self._folder and True or False

    def servicos(self):
        ct = self._ct
        folder_path = '/'.join(self._folder.getPhysicalPath())
        portal_types = ['Link', ]
        results = ct.searchResults(portal_type=portal_types,
                                   path=folder_path,
                                   sort_on='getObjPositionInParent')
        return results


class RedesSociaisViewlet(ViewletBase):
    ''' Viewlet de redes sociais
    '''
    # Indica qual o template sera usado por este viewlet
    index = ViewPageTemplateFile('templates/redessociais.pt')

    redes = []

    def update(self):
        ''' Prepara/Atualiza os valores utilizados pelo Viewlet
        '''
        super(RedesSociaisViewlet, self).update()
        tools = self.context.restrictedTraverse('@@plone_tools')
        pp = tools.properties()
        url = tools.url()
        portal_url = url()
        configs = getattr(pp, 'brasil_gov', None)
        redes = {}
        for rede in REDES:
            redes[rede['id']] = rede
        if configs:
            data = configs.getProperty('social_networks', [])
            selected = []
            for item in data:
                k, v = item.split('|')
                rede_info = redes[k]
                selected.append({'site': k,
                                 'info': v,
                                 'icon': '%s/%s' % (portal_url,
                                                    rede_info['icon']),
                                 'url': rede_info['url'] % v})
            self.redes = selected

    def available(self):
        return self.redes and True or False
