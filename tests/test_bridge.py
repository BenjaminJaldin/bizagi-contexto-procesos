import asyncio
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

SCRIPTS = Path(__file__).resolve().parents[1] / 'skills/bizagi-contexto-procesos/scripts'
sys.path.insert(0, str(SCRIPTS))
from modeler_bridge import ModelerBridge


def make_model(path, label='Revisar solicitud'):
    # Entirely synthetic: no customer data.
    xml = f'''<Package xmlns="http://www.wfmc.org/2009/XPDL2.2" Id="demo" Name="Proceso de ejemplo">
    <WorkflowProcesses><WorkflowProcess Id="process"><Activities>
    <Activity Id="start" Name="Inicio"><Event><StartEvent/></Event></Activity>
    <Activity Id="task" Name="{label}"><Implementation><Task/></Implementation></Activity>
    <Activity Id="end" Name="Fin"><Event><EndEvent/></Event></Activity>
    </Activities><Transitions><Transition Id="t1" From="start" To="task"/>
    <Transition Id="t2" From="task" To="end"/></Transitions></WorkflowProcess></WorkflowProcesses></Package>'''
    nested = io.BytesIO()
    with zipfile.ZipFile(nested, 'w') as z:
        z.writestr('Diagram.xml', xml.encode())
    with zipfile.ZipFile(path, 'w') as z:
        z.writestr('demo.diag', nested.getvalue())


class BridgeTests(unittest.TestCase):
    def test_saved_changes_and_company_isolation(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'example.bpm'
            make_model(p)
            b = ModelerBridge(folder)
            first = b.attach('example.bpm', 'Empresa ficticia')
            self.assertEqual(first['diagrams'][0]['activities'], 3)
            self.assertFalse(b.refresh()['changed_since_last_read'])
            make_model(p, 'Aprobar solicitud')
            self.assertTrue(b.refresh()['changed_since_last_read'])
            self.assertNotEqual(first['sha256'], b.refresh()['sha256'])
            b.attach('example.bpm')
            self.assertIsNone(b.refresh()['company_user_supplied'])
            self.assertEqual(b.get_diagram('demo')['diagram']['connections'][0]['source'], 'start')

    def test_scope_and_no_implicit_selection(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / 'allowed'
            root.mkdir()
            make_model(Path(folder) / 'outside.bpm')
            b = ModelerBridge(root)
            with self.assertRaises(ValueError):
                b.attach('../outside.bpm')
            with self.assertRaises(ValueError):
                b.refresh()

    def test_stdio_protocol(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        async def run(folder):
            params = StdioServerParameters(command=sys.executable,
                args=[str(SCRIPTS / 'modeler_bridge.py'), '--root', folder])
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    listing = await session.list_tools()
                    self.assertEqual({t.name for t in listing.tools},
                        {'modeler_status', 'attach_model', 'refresh_model', 'get_diagram', 'open_model'})
                    status = await session.call_tool('modeler_status', {})
                    self.assertFalse(status.isError)
                    attached = await session.call_tool('attach_model', {'model_path': 'example.bpm'})
                    self.assertFalse(attached.isError)
                    refreshed = await session.call_tool('refresh_model', {})
                    self.assertFalse(refreshed.isError)
                    make_model(Path(folder) / 'example.bpm', 'Solicitud actualizada')
                    updated = await session.call_tool('refresh_model', {})
                    self.assertFalse(updated.isError)
                    payload = json.loads(updated.content[0].text)
                    self.assertTrue(payload['changed_since_last_read'])
                    fetched = await session.call_tool('get_diagram', {'diagram_id': 'demo'})
                    self.assertFalse(fetched.isError)
                    bad = await session.call_tool('get_diagram', {'diagram_id': 'absent'})
                    self.assertTrue(bad.isError)
        with tempfile.TemporaryDirectory() as folder:
            make_model(Path(folder) / 'example.bpm')
            asyncio.run(run(folder))


if __name__ == '__main__':
    unittest.main()
