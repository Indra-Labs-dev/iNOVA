// Gate 5 UI — see docs/08-modules/news-intelligence.md. Extractive digest
// only: title/excerpt/source/date/link exactly as the source provides them
// — no AI-generated summary anywhere (deferred, see
// docs/adr/0014-defer-ai-summarization.md). Deliberately minimal: a list
// and a Refresh button, no categories/personalization/watchlists.
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../../core/auth/auth_session.dart';
import '../../../core/theme/inova_spacing.dart';
import '../../../shared/widgets/primary_button.dart';
import '../application/news_controller.dart';
import '../application/news_state.dart';
import '../data/news_item.dart';

class NewsScreen extends ConsumerWidget {
  const NewsScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final session = ref.watch(authSessionProvider);

    return Scaffold(
      appBar: AppBar(title: const Text('News Digest')),
      body: SafeArea(
        child: session.isAuthenticated ? const _DigestBody() : const _SignInHint(),
      ),
    );
  }
}

class _SignInHint extends StatelessWidget {
  const _SignInHint();

  @override
  Widget build(BuildContext context) {
    return const Center(child: Text('Sign in on the Research screen first, then come back here.'));
  }
}

class _DigestBody extends ConsumerStatefulWidget {
  const _DigestBody();

  @override
  ConsumerState<_DigestBody> createState() => _DigestBodyState();
}

class _DigestBodyState extends ConsumerState<_DigestBody> {
  bool _loaded = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) => _maybeLoad());
  }

  void _maybeLoad() {
    if (_loaded) return;
    _loaded = true;
    ref.read(newsControllerProvider.notifier).load();
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(newsControllerProvider);

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.all(INovaSpacing.md),
          child: PrimaryButton(
            label: 'Refresh',
            isLoading: state.status == NewsScreenStatus.refreshing,
            onPressed: () => ref.read(newsControllerProvider.notifier).refresh(),
          ),
        ),
        Expanded(child: _DigestList(state: state)),
      ],
    );
  }
}

class _DigestList extends StatelessWidget {
  const _DigestList({required this.state});

  final NewsState state;

  @override
  Widget build(BuildContext context) {
    if (state.status == NewsScreenStatus.loading) {
      return const Center(child: Text('Loading the digest…'));
    }
    if (state.status == NewsScreenStatus.error) {
      return Center(
        child: Text(
          state.errorMessage ?? 'Something went wrong.',
          style: const TextStyle(color: Colors.redAccent),
        ),
      );
    }
    if (state.items.isEmpty) {
      return const Center(child: Text('No items yet — tap Refresh to fetch the latest.'));
    }

    return ListView.builder(
      padding: const EdgeInsets.symmetric(horizontal: INovaSpacing.md),
      itemCount: state.items.length,
      itemBuilder: (context, index) => _NewsCard(item: state.items[index]),
    );
  }
}

class _NewsCard extends StatelessWidget {
  const _NewsCard({required this.item});

  final NewsItem item;

  @override
  Widget build(BuildContext context) {
    return Container(
      key: const Key('news-item'),
      margin: const EdgeInsets.only(bottom: INovaSpacing.md),
      padding: const EdgeInsets.all(INovaSpacing.md),
      decoration: BoxDecoration(
        color: Colors.white.withValues(alpha: 0.06),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(item.title, style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: INovaSpacing.xs),
          Text(
            [item.sourceName, if (item.publishedAt != null) _formatDate(item.publishedAt!)].join(' • '),
            style: const TextStyle(fontSize: 12, color: Colors.white70),
          ),
          if (item.excerpt != null && item.excerpt!.isNotEmpty) ...[
            const SizedBox(height: INovaSpacing.sm),
            Text(item.excerpt!),
          ],
          const SizedBox(height: INovaSpacing.sm),
          SelectableText(item.link, style: const TextStyle(fontSize: 12, color: Colors.blueAccent)),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) => date.toIso8601String().split('T').first;
}
