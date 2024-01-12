from argparse import ArgumentParser
from wiliot_deployment_tools.gw_certificate.gw_certificate import GWCertificate

def main():
    parser = ArgumentParser(prog='wlt-gw-certificate',
                            description='Gateway Certificate - CLI Tool to test Wiliot GWs')
    required = parser.add_argument_group('required arguments')
    required.add_argument('-owner', type=str, help="Owner ID", required=True)
    required.add_argument('-gw', type=str, help="Gateway ID", required=True)
    
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument('-suffix', type=str, help="Topic suffix", default='', required=False)
    optional.add_argument('-coupled', action='store_true', help="GW Metadata Coupling Enabled", default='False', required=False)

    
    args = parser.parse_args()
    topic_suffix = '' if args.suffix == '' else '-'+args.suffix
    gwc = GWCertificate(gw_id=args.gw, owner_id=args.owner, coupled=args.coupled,topic_suffix=topic_suffix)
    gwc.run_tests()
    gwc.create_results_html()

def main_cli():
    main()

if __name__ == '__main__':
    main()
