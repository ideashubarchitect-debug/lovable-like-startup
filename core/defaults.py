"""Default section content per app template."""

LANDING_SECTIONS = [
    {
        'type': 'hero',
        'title': 'Ship your product faster',
        'subtitle': 'Build, deploy, and iterate. No DevOps required.',
        'cta_text': 'Get started',
        'cta_url': '#',
    },
    {
        'type': 'features',
        'heading': 'Why us',
        'items': [
            {'title': 'Deploy in one click', 'description': 'Push to KloudBean and go live.'},
            {'title': 'Your brand', 'description': 'Your domain, your pricing, your customers.'},
            {'title': 'Scale when you need', 'description': 'Start free, upgrade when you grow.'},
        ],
    },
    {
        'type': 'pricing',
        'heading': 'Simple pricing',
        'subheading': 'Start free. Upgrade when you need more.',
        'plans': [
            {'name': 'Starter', 'price': '$0', 'period': 'forever', 'features': ['3 projects', 'Community support'], 'cta': 'Get started'},
            {'name': 'Pro', 'price': '$29', 'period': '/mo', 'features': ['Unlimited projects', 'Priority support', 'Custom domain'], 'cta': 'Start trial', 'highlight': True},
        ],
    },
    {
        'type': 'cta',
        'title': 'Ready to launch?',
        'subtitle': 'Join thousands of makers who ship on KloudBean.',
        'cta_text': 'Create account',
        'cta_url': '#',
    },
]

SAAS_SECTIONS = [
    {
        'type': 'hero',
        'title': 'The platform that scales with you',
        'subtitle': 'From idea to production in minutes. Built for startups.',
        'cta_text': 'Start free trial',
        'cta_url': '#',
    },
    {
        'type': 'features',
        'heading': 'Everything you need',
        'items': [
            {'title': 'Instant deploy', 'description': 'Connect repo, get a live URL.'},
            {'title': 'Database included', 'description': 'MySQL and more. No extra setup.'},
            {'title': 'SSL & security', 'description': 'HTTPS and env vars out of the box.'},
        ],
    },
    {
        'type': 'pricing',
        'heading': 'Plans',
        'subheading': 'Pick the right plan for your stage.',
        'plans': [
            {'name': 'Hobby', 'price': '$0', 'period': '', 'features': ['1 app', '512MB RAM'], 'cta': 'Free'},
            {'name': 'Pro', 'price': '$29', 'period': '/mo', 'features': ['5 apps', '2GB RAM', 'Custom domain'], 'cta': 'Try free', 'highlight': True},
            {'name': 'Team', 'price': '$99', 'period': '/mo', 'features': ['Unlimited apps', 'Priority support'], 'cta': 'Contact sales'},
        ],
    },
    {
        'type': 'cta',
        'title': 'Ready to build?',
        'subtitle': 'Deploy on KloudBean and own your stack.',
        'cta_text': 'Get started',
        'cta_url': '#',
    },
]

PORTFOLIO_SECTIONS = [
    {
        'type': 'hero',
        'title': 'Designer & Developer',
        'subtitle': 'I build products and experiences that ship.',
        'cta_text': 'View work',
        'cta_url': '#work',
    },
    {
        'type': 'features',
        'heading': 'What I do',
        'items': [
            {'title': 'Web apps', 'description': 'Full-stack and front-end.'},
            {'title': 'APIs & backends', 'description': 'Django, Node, and more.'},
            {'title': 'Consulting', 'description': 'Architecture and delivery.'},
        ],
    },
    {
        'type': 'cta',
        'title': 'Let\'s work together',
        'subtitle': 'Have a project in mind? Get in touch.',
        'cta_text': 'Contact me',
        'cta_url': '#',
    },
]


def get_default_sections(template):
    if template == 'saas':
        return [s.copy() for s in SAAS_SECTIONS]
    if template == 'portfolio':
        return [s.copy() for s in PORTFOLIO_SECTIONS]
    return [s.copy() for s in LANDING_SECTIONS]
